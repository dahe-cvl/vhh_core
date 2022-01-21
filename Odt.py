from vhh_od.OD import OD
import os
import yaml


class Odt(object):
    """
    This class includes the interfaces and methods to use the plugin package ODT.
    """

    def __init__(self, config=None):
        """
        Constructor

        :param config: parameter must hold the core configuration object (Class-type Configuration)
        """

        print("Create instance of odt")

        if (config == None):
            print("You have to specify a valid configuration instance!")

        # load configurations specified in core config file
        self.__core_config = config
        self.__odt_config_file = self.__core_config.odt_config_file
        self.__stc_config_file = self.__core_config.stc_config_file
        self.__video_download_path = self.__core_config.video_download_path

        # initialize odt plugin
        self.__od_instance = OD(self.__odt_config_file)

        fp = open(self.__core_config.stc_config_file, 'r')
        stc_config = yaml.load(fp, Loader=yaml.BaseLoader)
        self.__stc_results_dir = stc_config['StcCore']['PATH_FINAL_RESULTS']
        fp.close()

    def run(self, video_instance_list=None):
        """
        This method is used to run the object detection and tracking task.
        
        :param video_instance_list: parameter must hold a list of video objects (Class-type: Video)
        """

        print("start odt process ... ")

        for video_instance in video_instance_list:
            vid = video_instance.id
            stc_results_file = os.path.join(self.__stc_results_dir, str(vid) + ".csv")           
            shots_np = self.__od_instance.loadStcResults(stc_results_file)
            self.__od_instance.runOnSingleVideo(shots_per_vid_np=shots_np, max_recall_id=vid)
       
        print("odt process finished!")
