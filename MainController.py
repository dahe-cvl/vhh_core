from Sbd import Sbd
from Stc import Stc
from Cmc import Cmc
from VhhRestApi import VhhRestApi
from Configuration import Configuration
import numpy as np
import os
import csv
import json


class MainController(object):
    """
    This class represents the Main part of this application and includes all interfaces and methods to use the automatic annotation plugins.
    """

    def __init__(self):
        """
        Constructor
        """
        print("Create instance of MainController")

        # load CORE configuration
        config_file = "config/CORE/config.yaml"
        self.__configuration_instance = Configuration(config_file=config_file)
        self.__configuration_instance.loadConfig()

        if self.make_model_folders():
            print("Model folders have been created! Place your models into the respective directories.")
            exit()

        self.__root_url = self.__configuration_instance.root_url
        self.__pem_path = self.__configuration_instance.pem_path
        self.__video_download_path = self.__configuration_instance.video_download_path

        self.__sbd_config_file = self.__configuration_instance.sbd_config_file
        self.__stc_config_file = self.__configuration_instance.stc_config_file
        self.__cmc_config_file = self.__configuration_instance.cmc_config_file

        # initialize class members
        self.__sbd_instance = Sbd(config=self.__configuration_instance)
        self.__stc_instance = Stc(config=self.__configuration_instance)
        self.__cmc_instance = Cmc(config=self.__configuration_instance)

        self.__rest_api_instance = VhhRestApi(config=self.__configuration_instance)

        self.make_video_folder()
        self.make_result_folders()

    def run(self):
        """
        This method is used to start the automatic annotation process.
        """

        print("Start automatic annotation process ... ")

        # get list of videos in mmsi
        video_instance_list = self.__rest_api_instance.getListofVideos()
        #video_instance_list = video_instance_list[1:]

        # cleanup video and results folder
        if (self.__configuration_instance.cleanup_flag == 1):
            for video_instance in video_instance_list:
                video_instance.cleanup()

        # download videos if not available
        for video_instance in video_instance_list:
            if (video_instance.is_downloaded() == False):
                video_instance.download(self.__rest_api_instance)

        # run sbd
        if self.__configuration_instance.use_sbd:
            self.__sbd_instance.run(video_instance_list=video_instance_list)

        # run stc
        if self.__configuration_instance.use_stc:
            self.__stc_instance.run()

        # run cmc
        if self.__configuration_instance.use_cmc:
            self.__cmc_instance.run()

        # merge all results
        results_np = self.merge_results()
        header = ["vid_name", "shot_id", "start", "end", "stc", "cmc"]

        vids = np.unique(results_np[:, :1])
        print(vids)
        
        if self.__configuration_instance.results_format == "CSV_LOCAL":

            # write Output to .csv file
            csv_path = os.path.join(self.__configuration_instance.results_root_dir, "core", "results.csv")
            print(f"Writing results to \"{csv_path}\"...")
            with open(csv_path, 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=';')
                csv_writer.writerow(header)
                for row_idx in range(results_np.shape[0]):
                    csv_writer.writerow(results_np[row_idx, :])

        elif self.__configuration_instance.results_format == "JSON_LOCAL":
            data = {}
            data['analysis_results'] = []

            # create dictionary as basis for JSON file
            for vid in vids:
                indices = np.where(vid == results_np[:, 0])[0]
                vid_results_np = results_np[indices]

                vid_results_dict = {}
                vid_results_dict['vid_name'] = vid
                vid_results_dict['shots'] = []

                rows, cols = vid_results_np.shape
                for row_idx in range(rows):
                    result = {}
                    for col in range(cols):
                        if col is not 1:
                            result[header[col]] = vid_results_np[row_idx, col]
                    vid_results_dict['shots'].append(result)
                data['analysis_results'].append(vid_results_dict)

            # write JSON file
            json_path = os.path.join(self.__configuration_instance.results_root_dir, "core", "results.json")
            print(f"Writing results to \"{json_path}\"...")
            with open(json_path, 'w', newline='') as json_file:
                json.dump(data, json_file)


        elif self.__configuration_instance.results_format == "JSON_REST":
            print(f"Posting results using Rest API...")
            # post all results
            for vid in vids:
                indices = np.where(vid == results_np[:, 0])[0]
                vid_results_np = results_np[indices]

                header_np = np.expand_dims(np.array(header), axis=0)
                vid_results_np = np.concatenate((header_np, vid_results_np), axis=0)
                print(vid_results_np)
                self.__rest_api_instance.postAutomaticResults(vid=int(vid.split('.')[0]), results_np=vid_results_np)

        else:
            print("No results were written.")
            print("If you wish to write any output, please set the RESULTS_FORMAT in the Config file.")

        print("Successfully finished!")

    def merge_results(self):
        """
        This method is used to merge and prepare the results of each individual plugin (sbd, stc, cmc) to send it to the the Vhh-MMSI database.

        :return: This method returns a numpy array holding all results (including a valid header).
        """
        # merge and prepare results
        sbd_results_path = os.path.join(self.__configuration_instance.results_root_dir, "sbd")
        sbd_results_path = os.path.join(sbd_results_path, "final_results")

        stc_results_path = os.path.join(self.__configuration_instance.results_root_dir, "stc")
        stc_results_path = os.path.join(stc_results_path, "final_results")

        cmc_results_path = os.path.join(self.__configuration_instance.results_root_dir, "cmc")
        cmc_results_path = os.path.join(cmc_results_path, "final_results")

        sbd_result_file_list = os.listdir(sbd_results_path)
        sbd_result_file_list = [os.path.join(sbd_results_path, x) for x in sbd_result_file_list]
        stc_result_file_list = os.listdir(stc_results_path)
        stc_result_file_list = [os.path.join(stc_results_path, x) for x in stc_result_file_list]
        cmc_result_file_list = os.listdir(cmc_results_path)
        cmc_result_file_list = [os.path.join(cmc_results_path, x) for x in cmc_result_file_list]

        entries = []
        for results_file in sbd_result_file_list:
            fp = open(results_file)
            lines = fp.readlines()
            fp.close()

            for line in lines[1:]:
                line = line.replace('\n', '')
                line_split = line.split(';')
                entries.append([line_split[0].split('.')[0],
                                line_split[1],
                                line_split[2],
                                line_split[3]])
        sbd_entries_np = np.array(entries)
        print(sbd_entries_np)

        entries = []
        for results_file in stc_result_file_list:
            fp = open(results_file)
            lines = fp.readlines()
            fp.close()

            for line in lines[1:]:
                line = line.replace('\n', '')
                line_split = line.split(';')

                # TODO: just a temporary workaround
                #if (line_split[4] == 'I'):
                #    line_split[4] = 'NA'
                entries.append([line_split[0].split('.')[0],
                                line_split[1],
                                line_split[2],
                                line_split[3],
                                line_split[4]])
        stc_entries_np = np.array(entries)
        print(stc_entries_np)

        entries = []
        for results_file in cmc_result_file_list:
            fp = open(results_file)
            lines = fp.readlines()
            fp.close()

            for line in lines[1:]:
                line = line.replace('\n', '')
                line_split = line.split(';')
                entries.append([line_split[0].split('.')[0],
                                line_split[1],
                                line_split[2],
                                line_split[3],
                                line_split[4]])
        cmc_entries_np = np.array(entries)
        print(cmc_entries_np)
        

        if(len(stc_entries_np) > 0 and len(cmc_entries_np) > 0):
            entries_np = np.concatenate((sbd_entries_np, stc_entries_np[:, 4:]), axis=1)
            entries_np = np.concatenate((entries_np, cmc_entries_np[:, 4:]), axis=1)
        else:
            dummy_entries_np = np.empty([len(sbd_entries_np), 1]).astype('str')
            dummy_entries_np[:] = "NA"
            entries_np = np.concatenate((sbd_entries_np, dummy_entries_np), axis=1)
            entries_np = np.concatenate((entries_np, dummy_entries_np), axis=1)
        print(entries_np)
        return entries_np

    def make_result_folders(self):

        results_root_dir = self.__configuration_instance.results_root_dir
        plugins = ["sbd", "stc", "cmc"]
        results_sub_dirs = ["raw_results", "final_results", "develop"]

        try: os.mkdir(results_root_dir)
        except OSError: pass

        for plugin in plugins:
            for sub_dir in results_sub_dirs:
                try: os.makedirs(os.path.join(results_root_dir, plugin, sub_dir))
                except OSError: pass

        try: os.mkdir(os.path.join(results_root_dir, "core"))
        except OSError: pass

    def make_video_folder(self):
        video_root_dir = self.__configuration_instance.video_download_path
        try: os.mkdir(video_root_dir)
        except OSError: pass

    def make_model_folders(self):

        model_root_dir = self.__configuration_instance.model_path
        plugins = ["sbd", "stc", "cmc"]

        try: os.mkdir(model_root_dir)
        except OSError: return False

        for plugin in plugins:
            try: os.makedirs(os.path.join(model_root_dir, plugin))
            except OSError: return False

        return True
