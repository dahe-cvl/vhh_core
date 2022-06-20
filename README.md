# vhh_core

This package represents the Automatic Video Analysis Framework (AVAF) for the H2020 project Visual History of the 
Holocaust. It includes various video analysis techniques (e.g. Shot Boundary Detection, Shot Type Classfication and 
Camera Movements Classification).

## Package Description

PDF format: [vhh_core_pdf](https://github.com/dahe-cvl/vhh_core/blob/master/ApiSphinxDocumentation/build/latex/vhhcorepackageautomaticvideoanalysisframeworkvhh_core.pdf)
    
HTML format (only usable if repository is available in local storage): [vhh_core_html](https://github.com/dahe-cvl/vhh_core/blob/master/ApiSphinxDocumentation/build/html/index.html)

## Quick Setup

**Requirements:**

   * Ubuntu 18.04 LTS
   * python version 3.6.x

**Create a virtual environment:**

   * create a folder to a specified path (e.g. /xxx/vhh_core/)
   * ```python3 -m venv /xxx/vhh_core/```

**Activate the environment:**

   * ```source /xxx/vhh_core/bin/activate```

**Checkout vhh_core repository to a specified folder:**

   * ```git clone https://github.com/dahe-cvl/vhh_core```

**Install dependencies and plugins**

   * ```cd /xxx/vhh_core/```
   * ```pip install -r requirements.txt```
    
**Install PyTorch**

Install a Version of PyTorch depending on your setup. Consult the [PyTorch website](https://pytorch.org/get-started/locally/) for detailed instructions.

**Setup environment variables:**

   * Activate environment: ```source /xxx/vhh_core/bin/activate```
   * Let PATH_TO_DIR be the path to the directory containing this repository. Change pythonpath:
    ```export PYTHONPATH=$PYTHONPATH:/PATH_TO_DIR/vhh_core/:/PATH_TO_DIR/vhh_core/Develop/:/PATH_TO_DIR/vhh_core/Demo/```
   
**Import Models**

Executing the program for the first time (see next section) will create the desired folder structure. Insert the models for SBD and STC into the corresponding subdirectories of ```/models```.
Folders for the downloaded videos and the results will be automatically created in the second run.
   
**Run demo script**

   * change to root directory of the repository
   * ```python Demo/run_automatic_annotation_process.py```
   * Import models for SBD and STC.
   * ```python Demo/run_automatic_annotation_process.py```


## Helpful Scripts
The `Develop` folder contains a variety of useful scripts. Here we just include a short description of each, for more information check the description at the start of each script or run them with the `-h` parameter.

* `compare_videos.py` Creates a side-by-side comparison of two given videos
* `download_annotation_results.py` Download shot based video annotation results from VhhMMSI 
* `download_relations.py` Download relation annotations from VhhMMSI
* `download_video_metadata.py` Download video metadata from VhhMMSI
* `download_videos.py` Download videos from VhhMMSI
* `generate_sequences_from_relations.py` Extract video sequences from relations annotations
* `post_cmc_results.py` Upload a camera annotation from vhh_core to VhhMMSI
* `post_od_results.py` Upload an object detection annotation from vhh_core to VhhMMSI