import libtools, os, sys
from importlib import import_module

class Addon():
    def __init__(self, logger, appinfo):
        self.loaded_addon={}
        self.loaded_addon_info={}
        self.extdict={}
        self.logger=logger
        self.appinfo=appinfo
    def install(self):
        pass
    def uninstall(self):
        pass
    def load(self, addon_file, addon_type):
        try:
            module=import_module(os.path.splitext(os.path.basename(addon_file))[0], os.path.dirname(addon_file).replace(os.path.sep, "."))
        except:
            self.logger.warn(f"Can't import addon({addon_file}). (Not a collect python file.)")
            return False
        if addon_type == "editor" and hasattr(module, "Edit"):
            if not callable(module.Edit):
                self.logger.warn(f"Can't import addon({addon_file}). (Edit class is not callable.)")
                return False
            attrs=["name", "file_types", "save", "close", "new"]
            addon=module.Edit
            for attr in attrs:
                if not hasattr(addon, attr):
                    self.logger.warn(f"Can't import addon({addon_file}). (Missing {attr} attr.)")
                    break
            else:
                if addon.name in self.loaded_addon:
                    self.logger.warn(f"Can't import addon({addon_file}). (Used addon name.)")
                    return False
                self.loaded_addon[addon.name]=addon
                self.loaded_addon_info[addon.name]={"name":addon.name,"filetypes":addon.file_types}
                for ext in addon.file_types:
                    if not ext in self.extdict:
                        self.extdict[ext]=[]
                    self.extdict[ext].append(addon.name)
                self.logger.debug(f"{addon.name} was loaded")
                return True
            return False
    def unload(self):
        pass
    def loadAll(self, load_dirs, addon_type, ignorelist=[]):
        sys.path.extend(load_dirs)
        for load_dir in load_dirs:
            for addon_file in os.listdir(load_dir):
                addon_path=os.path.join(load_dir, addon_file)
                if not addon_path in ignorelist:
                    self.load(addon_file=addon_path, addon_type=addon_type)
        self.logger.info(f'{list(self.loaded_addon.keys())} was loaded.')
    def getAddon(self, addon, filepath, ext, ui, app):
        api=AddonAPI(addon, self.appinfo, filepath, ext, ui, app)
        addon_ctx=self.loaded_addon[addon](api)
        api.addon=addon_ctx
        return api
class AddonAPI(object):
    def __init__(self, name, appinfo, filepath, ext, ui, app):
        self.name=name
        self.logger=libtools.core.Logger(name=name, log_dir=appinfo["log"])
        self.appinfo=appinfo
        self.filepath=filepath
        self.ext=ext
        self.ui=ui
        self.app=app
        self.saved=True
        self.api_ver=0
        self.api_ver_minor=0
    def __setattr__(self, __name, __value):
        super().__setattr__(__name, __value)
        if __name == "saved":
            self.app.update_state()
    def getConfig(self, module="main", default_conf={}):
        self.config=libtools.Config(appname=self.name, module=module, default_conf=default_conf, addon=self.appinfo)