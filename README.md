# TrackingNet-devkit

Development kit for the dataset **TrackingNet: A Large-Scale Dataset and
Benchmark for Object Tracking in the Wild**.

Compete in our benchmark by submitting your result on our [evaluation server](http://eval.tracking-net.org).

For more details, please refer to our [paper](https://ivul.kaust.edu.sa/Documents/Publications/2018/TrackingNet%20A%20Large%20Scale%20Dataset%20and%20Benchmark%20for%20Object%20Tracking%20in%20the%20Wild.pdf).

```
@InProceedings{Muller_2018_ECCV,
author = {Muller, Matthias and Bibi, Adel and Giancola, Silvio and Alsubaihi, Salman and Ghanem, Bernard},
title = {TrackingNet: A Large-Scale Dataset and Benchmark for Object Tracking in the Wild},
booktitle = {The European Conference on Computer Vision (ECCV)},
month = {September},
year = {2018}
}
```




# Structure of the dataset
There are 12 chunks of 2511 sequences for the training and 1 chunk of 511 sequences for the testing.

Each chunk have subfolders for the zipped sequence (`zips`), the unzipped frame (`frames`) and eventually the annotation (`anno`).

The structure of the dataset is the following:
```
TrackingNet
 - Test / Train_X (with X from 0 to 11)
   - zips
   - frames
   - anno (Test: annotation only for 1st frame)
```



# Create the environment

Tested on Ubuntu 16.04 LTS


 - Create the environment:

`conda env create -f environment.yml`

or (preferred for other platforms)

`conda create -n TrackingNet python=3 requests pandas tqdm numpy`

 - Activate the environment:

`source activate TrackingNet` (`activate TrackingNet` for windows platforms)



# Download the dataset

You can download the whole dataset by running:

`python download_TrackingNet.py --trackingnet_dir <trackingnet_dir>`

### Optional parameters:
  - `--trackingnet_dir`: path where to download the TrackingNet dataset
  - `--data` select the data to download (sequences: `--data zips` / annotations: `--data anno`)
  - `--chunk` select the chunk to download (testing set: `--chunk Test` / training set: `--chunk Train` / selected chunks: `--chunk 0,2,4,11`)
 
Please look at `python download_TrackingNet.py --help` for more details on the optional parameters.


### Disclaimer

In case an error such as `Permission denied: https://drive.google.com/uc?id=<ID>, Maybe you need to change permission over 'Anyone with the link'?` occurs, please check your internet connection and run again the script.
The script will not overwrite the previous sequences of videos if are already completely downloaded.

Note that Google Drive limits the download bandwidth to ~10TB/day. To ensure a good share between all users, avoid downloading the dataset several times and prefer sharing it with your colleagues using an old-fashion HDD.

### [Update from 25-02-2020]: Back up links

To anyone who still has issue downloading TrackingNet, we are currently trying to find more reliable solutions. For now, we have created back up links to download full chunks of training (and the testing chunk). It's still hosted on Google Drive, but will be easier to spread around the community using alternative sharing platforms (e.g. Baidu, Dropbox, good old HDD,...).

Here are two back up links: [[link1](https://drive.google.com/drive/u/2/folders/1gJOR-r-jPFFFCzKKlMOW80WFtuaMiaf6)] [[link2](https://drive.google.com/drive/u/2/folders/1xrxlI6otQvWlRJjsX1pddZBY9h2WbmVi)]

Now, it appears that Google Drive is limiting the download if you are not signed in with you gmail account. If you have any issue downloading it, please make sure you are signed in google drive with you gmail account. We will track the situation in the next days.


# Unzip the frames

To extract all the zipped sequences for the complete dataset:

`python extract_frame.py --trackingnet_dir <trackingnet_dir>`

### Optional parameters:
  - `--trackingnet_dir`: path where to download the TrackingNet dataset
  - `--chunk`: select the chunk to download (testing set: `--chunk Test` / training set: `--chunk Train` / selected chunks: `--chunk 0,2,4,11`)
  
### Disclaimer
In this step, make sure you don't have any error message.
You can run this script several times to make sure all the files are properly extracted. 
By default, the unzipping script will not overwrite the frames that are properly extracted.

If any zip file is currupted, a error message will appear `Error: the zip file [zip_file_name] is corrupted`. 
In thas case, remove the corrupted zip file manually and run the download script again. 
By default, the download script will not overwrite the zip files already downloaded.
 


# (Optional) Generate Frames with the annotation boundingboxes

This part requires `opencv`: `conda install -c menpo opencv`

To generate the BB in the frames for the complete dataset:

`python generate_BB_frames.py --output_dir <trackingnet_dir>`

### Optional parameters:
  - `--output_dir`: path where to generate the images with boundingboxes
  - `--chunk` select the chunk to download (testing set: `--chunk Test` / training set: `--chunk Train` / selected chunks: `--chunk 0,2,4,11`)


# Evaluate the results of a tracker with a given ground truth

If you plan to submit results on our [evaluation server](http://eval.tracking-net.org), you may want to validate your results first.

The evaluation code we are using is available on `metrics.py`, whhich can be used as following:

`python metrics.py --GT_zip <GT.zip> --subm_zip <subm.zip>`

A dummy example of file is provided here:

`python metrics.py --GT_zip dummy_GT.zip --subm_zip dummy_subm.zip`



