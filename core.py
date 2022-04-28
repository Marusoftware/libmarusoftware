import sys, os, platform, logging, random, string

def randomstr(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

def adjustEnv(logger, appinfo):
    #change macOS Bundle name
    if getattr(sys, "frozen", False) and appinfo["os"] == "Darwin":
        try:
            from Foundation import NSBundle
            bundle = NSBundle.mainBundle()
            if bundle:
                info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
                if info and info['CFBundleName'] == 'Python':
                    info['CFBundleName'] = appinfo["appname"].lower()
        except:
            logger.debug("Error was happen on changeing MacOS ProcessName")
        else:
            logger.debug("MacOS ProcessName was succesfully changed.")
    sys.dont_write_bytecode = True# __pycache__ deletion
    #path setting
    if not appinfo["share"] in sys.path:
        sys.path.append(appinfo["share"])#share library path
    if not appinfo["share_os"] in os.environ["PATH"]:
        os.environ["PATH"] += ":"+appinfo["share_os"]
    if not appinfo["share_os"] in sys.path:
        sys.path.append(appinfo["share_os"])
    if platform.system() == "Windows":
        #Hi DPI Support
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(True)
        logger.debug("HiDPI Support is enabled.")
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appinfo["appname"])
        logger.debug("Icon changing was fixed.")

class Logger():
    def __init__(self, log_dir, name="", log_level=0):
        log_dir=os.path.join(log_dir, name)
        os.makedirs(log_dir ,exist_ok=True)
        print("Start Logging on ",os.path.join(log_dir, str(len(os.listdir(log_dir))+1)+".log"))
        logging.basicConfig(format='%(levelname)s:%(asctime)s:%(name)s| %(message)s',level=log_level)
        logger = logging.getLogger(name)
        logger.stdErrOut= logging.StreamHandler()
        logger.stdErrOut.setLevel(log_level)
        logger.stdErrOut.setFormatter(logging.Formatter('%(levelname)s:%(asctime)s:%(name)s| %(message)s'))
        logger.fileOut= logging.FileHandler(os.path.join(log_dir, str(len(os.listdir(log_dir))+1)+".log"))
        logger.fileOut.setLevel(log_level)
        logger.fileOut.setFormatter(logging.Formatter('%(levelname)s:%(asctime)s:%(name)s| %(message)s'))
        logger.addHandler(logger.fileOut)
        self.logger=logger
        self.childs=[]
    def getChild(self, name):
        child=self.logger.getChild(name)
        self.childs.append(child)
        return child
    def info(self, text):
        self.logger.info(text)
    def error(self, text):
        self.logger.error(text)
    def warn(self, text):
        self.logger.warn(text)
    def critical(self, text):
        self.logger.critical(text)
    def exception(self, text):
        self.logger.exception(text)
    def debug(self, text):
        self.logger.debug(text)