# TrackingNet-devkit

Development kit for TrackingNet


# Structure of the dataset
There are 12 chunks of 2511 sequences for the training and 1 chunk of 511 sequences for the testing.

Each chunk have subfolders for the zipped sequence (`zips`), the unzipped frame (`frames`) and eventually the annotation (`anno`).

The structure of the dataset is the following:
```
TrackingNet
 - Test
   - zips
   - frames
 - Train_X (with X from 0 to 11)
   - zips
   - frames
   - anno
```



# Create the environment

Tested on Ubuntu 16.04 LTS


 - Create the environment:

`conda env create -f environment.yml`

or

`conda create -n TrackingNet python=3 requests pandas tqdm numpy`

 - Activate the environment:

`source activate TrackingNet`



# Download the dataset

You can download the whole dataset by running:

`python download_TrackingNet.py --trackingnet_dir <trackingnet_dir>`
 

## Download the zipped sequences / annotations only `--data`

To download all the zipped files:

`python download_TrackingNet.py --trackingnet_dir <trackingnet_dir> --data zips`

To download all the annotation files:

`python download_TrackingNet.py --trackingnet_dir <trackingnet_dir> --data anno`



## Download a specific chunk of the dataset (TEST / TRAIN from 0 to 11) `--chunk`

To download the testing set only:

`python download_TrackingNet.py --trackingnet_dir <trackingnet_dir> --chunk Test`

To download the training set only:

`python download_TrackingNet.py --trackingnet_dir <trackingnet_dir> --chunk Train`

To download a few chunk of the training set only (here chunks 0, 2, 4 and 11):

`python download_TrackingNet.py --trackingnet_dir <trackingnet_dir> --chunk 0,2,4,11`


## Combination of the 2 previous options

To download the annotations for a few chunk of the training set only:

`python download_TrackingNet.py --trackingnet_dir <trackingnet_dir> --data anno --chunk 0,2,4,11`

Please look at `python download_TrackingNet.py --help` for more details. Note that we are not providing the annotations for the testing set.


## Disclaimer

In case an error such as `Permission denied: https://drive.google.com/uc?id=<ID>, Maybe you need to change permission over 'Anyone with the link'?` occurs, check your internet connection and run again the script.
The script will not overwrite the previous sequences of videos that are already downloaded.



# Unzip the frames

To extract all the zipped sequences for the complete dataset:

`python extract_zip.py --trackingnet_dir <trackingnet_dir>`

To extract the zipped sequences for a few chunk of the dataset (here chunks 0, 2, 4 and 11):

`python extract_zip.py --trackingnet_dir <trackingnet_dir> --chunk 0,2,4,11`

In this step, make sure you don't have any error message.
You can run this script several times to make sure all the files are properly extracted. 
By default, the unzipping script will not overwrite the frames that are properly extracted.

If any zip file is currupted, a error message will appear `Error: the zip file [zip_file_name] is corrupted`. 
In thas case, remove the corrupted zip file manually and run the download script again. 
By default, the download script will not overwrite the zip files already downloaded.
 


# (Optional) Generate Frames with the annotation boundingboxes

This part requires `opencv`:

`conda install -c menpo opencv`

To generate the BB in the frames for the complete dataset:

`python generate_BB_frames.py --output_dir <trackingnet_dir>`

To generate the BB in the frames for a few chunk of the complete dataset (here chunks 0, 2, 4 and 11):

`python generate_BB_frames.py --output_dir <trackingnet_dir> --chunk 0,2,4,11`


# Evaluate the results of a tracker with a given ground truth

If you plan to submit results on our [evaluation server](http://eval.tracking-net.org), you may want to validate your results first.

The evaluation code we are using is available on `metrics.py`, whhich can be used as following:

`python metrics.py --GT_zip <GT.zip> --subm_zip <subm.zip>`

A dummy example of file is provided here:

`python metrics.py --GT_zip dummy_GT.zip --subm_zip dummy_subm.zip`



