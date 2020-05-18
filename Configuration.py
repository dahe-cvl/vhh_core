from stc.utils import *
import yaml


class Configuration:
    """
    This class is needed to read the configuration parameters specified in the configuration.yaml file.
    The instance of the class is holding all parameters during runtime.

    .. note::
       e.g. ./config/config_vhh_test.yaml

        the yaml file is separated in multiple sections
        config['Development']
        config['PreProcessing']
        config['StcCore']
        config['Evaluation']

        whereas each section should hold related and meaningful parameters.
    """

    def __init__(self, config_file: str):
        """
        Constructor

        :param config_file: [required] path to configuration file (e.g. PATH_TO/config.yaml)
                                       must be with extension ".yaml"
        """
        printCustom("create instance of configuration ... ", STDOUT_TYPE.INFO)

        if(config_file.split('.')[-1] != "yaml"):
            printCustom("Configuration file must have the extension .yaml!", STDOUT_TYPE.ERROR)

        self.config_file = config_file

        self.debug_flag = -1
        self.pem_path = "None"
        self.root_url = "None"
        self.video_download_path = "None"
        self.sbd_config_file = "None"
        self.stc_config_file = "None"
        self.cmc_config_file = "None"
        self.cleanup_flag = False

    def loadConfig(self):
        """
        Method to load configurables from the specified configuration file
        """

        fp = open(self.config_file, 'r')
        config = yaml.load(fp, Loader=yaml.BaseLoader)

        developer_config = config['Development']
        security_config = config['Security']
        vhh_core_config = config['VhhCore']
        api_config = config['ApiEndpoints']
        plugin_config = config['PluginConfigs']

        # developer_config section
        self.debug_flag = int(developer_config['DEBUG_FLAG'])

        # security section
        self.pem_path = str(security_config['PEM_PATH'])

        # vhh_core_config section
        self.video_download_path = vhh_core_config['VIDEO_DOWNLOAD_PATH']
        self.cleanup_flag = int(vhh_core_config['CLEANUP_FLAG'])

        # plugin_config section
        self.sbd_config_file = str(plugin_config['SBD_CONFIG_FILE'])
        self.stc_config_file = plugin_config['STC_CONFIG_FILE']
        self.cmc_config_file = plugin_config['CMC_CONFIG_FILE']

        # api_config section
        self.root_url = api_config['ROOT_URL']

