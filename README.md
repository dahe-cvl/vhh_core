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

   * ```source /data/dhelm/python_virtenv/vhh_core_env/bin/activate```
   * ```export CUDA_VISIBLE_DEVICES=0```
   * ```export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-10.1/lib64/```
   * ```export CUDA_HOME=/usr/local/cuda-10.1```
   * ```export PATH=$PATH:/usr/local/cuda-10.1/bin```
   * ```export PYTHONPATH=$PYTHONPATH:/XXX/vhh_core/:/XXX/vhh_core/Develop/:/XXX/vhh_core/Demo/```
   * ```export PYTHONPATH=$PYTHONPATH:/home/dhelm/VHH_Releases/vhh_core/vhh_core/:/home/dhelm/VHH_Releases/vhh_core/vhh_core/Develop/:/home/dhelm/VHH_Releases/vhh_core/vhh_core/Demo/```
   
**Import Models**

Executing the program for the first time (see next section) will create the desired folder structure. Insert the models for SBD and STC into the corresponding subdirectories of ```/models```.
Folders for the downloaded videos and the results will be automatically created in the second run.
   
**Run demo script**

   * change to root directory of the repository
   * ```python Demo/run_automatic_annotation_process.py```
   * Import models for SBD and STC.
   * ```python Demo/run_automatic_annotation_process.py```

## Docker Setup instructions

NOT AVAILABLE YET