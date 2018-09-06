import os
import random
import sys
import traceback
import zipfile

import numpy as np
import pandas as pd

from tqdm import tqdm 



def evaluate(test_annotation_file, user_submission_file):


    # open zip file
    archive_anno = zipfile.ZipFile(test_annotation_file, 'r')
    archive_subm = zipfile.ZipFile(user_submission_file, 'r')
    otb_files_anno = [name for name in archive_anno.namelist() if name.endswith('.txt') and "__MACOSX" not in name]
    otb_files_subm = [name for name in archive_subm.namelist() if name.endswith('.txt') and "__MACOSX" not in name]


    # pandaframe with all the OPE results
    df_all = pd.DataFrame(columns=["sanity_check","IoU","distance","ndistance"])
    n = 21
    Success_test_avg  = np.zeros(n)
    Precision_test_avg  = np.zeros(n)
    NPrecision_test_avg  = np.zeros(n)
    Success_X= np.linspace(0, 1, n)
    Precision_X = np.linspace(0, 50, n)
    NPrecision_X = np.linspace(0, 0.5, n)

    # loop over the annotation files
    for i, name_file_anno in tqdm(enumerate(otb_files_anno)):

        file = archive_anno.open(name_file_anno) 
        df = pd.read_csv(file, sep = ",", names = ["anno_x1","anno_y1","anno_w","anno_h"])

        name_file_subm = [s for s in otb_files_subm if os.path.basename(name_file_anno) in s]

        if(len(name_file_subm) == 1): # only 1 file
            file_subm = archive_subm.open(name_file_subm[0]) 
            df_subm = pd.read_csv(file_subm, sep = ",", names = ["subm_x1","subm_y1","subm_w","subm_h"])
            df["sanity_check"] = 1.0

            
        else:
            df_subm = pd.DataFrame(0, index=np.arange(len(df)), columns = ["subm_x1","subm_y1","subm_w","subm_h"])
            df["sanity_check"] = 0.0






        # copy submission to dataframe
        df["subm_x1"] = df_subm["subm_x1"]
        df["subm_y1"] = df_subm["subm_y1"]
        df["subm_w"] = df_subm["subm_w"]
        df["subm_h"] = df_subm["subm_h"]
        df["subm_w"] = np.round(df_subm["subm_w"].astype(float))
        df["subm_h"] = np.round(df_subm["subm_h"].astype(float))
        df["anno_w"] = np.round(df["anno_w"].astype(float))
        df["anno_h"] = np.round(df["anno_h"].astype(float))
        df["subm_x1"] = np.round(df_subm["subm_x1"].astype(float))
        df["subm_y1"] = np.round(df_subm["subm_y1"].astype(float))
        df["anno_x1"] = np.round(df["anno_x1"].astype(float))
        df["anno_y1"] = np.round(df["anno_y1"].astype(float))
       
        df.loc[0,"subm_x1"] = df.loc[0,"anno_x1"]
        df.loc[0,"subm_y1"] = df.loc[0,"anno_y1"]
        df.loc[0,"subm_w"] = df.loc[0,"anno_w"]
        df.loc[0,"subm_h"] = df.loc[0,"anno_h"]

        # from (x,y,w,h) to (x1,y1,x2,y2)
        df["anno_x2"] = df["anno_x1"] + df["anno_w"] - 1.0
        df["anno_y2"] = df["anno_y1"] + df["anno_h"] - 1.0
        df["subm_x2"] = df["subm_x1"] + df["subm_w"] - 1.0
        df["subm_y2"] = df["subm_y1"] + df["subm_h"] - 1.0

        # compute centers for BB
        df["anno_center_x"] = df["anno_x1"] + ( df["anno_w"] + 1.0 ) / 2.0
        df["anno_center_y"] = df["anno_y1"] + ( df["anno_h"] + 1.0 ) / 2.0
        df["subm_center_x"] = df["subm_x1"] + ( df["subm_w"] + 1.0 ) / 2.0
        df["subm_center_y"] = df["subm_y1"] + ( df["subm_h"] + 1.0 ) / 2.0

        # compute (x1,y1,x2,y2) of interection
        df["inter_x1"] = df[["anno_x1", "subm_x1"]].max(axis=1)
        df["inter_y1"] = df[["anno_y1", "subm_y1"]].max(axis=1)
        df["inter_x2"] = df[["anno_x2", "subm_x2"]].min(axis=1)
        df["inter_y2"] = df[["anno_y2", "subm_y2"]].min(axis=1)
             
        # compute the area of intersection rectangle
        df["inter_w"] = np.round(df["inter_x2"] - df["inter_x1"] + 1).clip(lower=0)
        df["inter_h"] = np.round(df["inter_y2"] - df["inter_y1"] + 1).clip(lower=0)
        df["inter_area"] = df["inter_w"] * df["inter_h"]
            
        df["subm_area"] = (df["subm_h"]) * (df["subm_w"])
        df["anno_area"] = (df["anno_h"]) * (df["anno_w"])




        df["sanity_check"] = (df["subm_h"] + df["subm_w"] + df["subm_x1"] + df["subm_y1"]) > 0

        df_all = df_all.append(df[["sanity_check"]])


        df.loc[df["sanity_check"] > 0, "IoU"] = -1.0


        # compute IoU
        df["IoU"] = df["inter_area"] / (df["anno_area"]+df["subm_area"]-df["inter_area"])

        # compute center distance
        df["distance"]  = ( (df["anno_center_x"] - df["subm_center_x"]) * 
                            (df["anno_center_x"] - df["subm_center_x"]) + 
                            (df["anno_center_y"] - df["subm_center_y"]) * 
                            (df["anno_center_y"] - df["subm_center_y"]) ).apply(np.sqrt)
        
        # compute center distance normalized over the GT BB dimension
        df["ndistance"] = ( (df["anno_center_x"] - df["subm_center_x"]) / df["anno_w"] * 
                            (df["anno_center_x"] - df["subm_center_x"]) / df["anno_w"] + 
                            (df["anno_center_y"] - df["subm_center_y"]) / df["anno_h"] * 
                            (df["anno_center_y"] - df["subm_center_y"]) / df["anno_h"] ).apply(np.sqrt)




        Success_test_avg += np.array([np.sum(i >= thres for i in df["IoU"]).astype(float) / (len(df["IoU"]))  for thres in Success_X]) 
        Precision_test_avg += np.array([np.sum(i <= thres for i in df["distance"]).astype(float) / (len(df["distance"]))  for thres in Precision_X]) 
        NPrecision_test_avg += np.array([np.sum(i <= thres for i in df["ndistance"]).astype(float) / (len(df["ndistance"]))  for thres in NPrecision_X]) 

        print(df.loc[df["IoU"] < 1.0])

  
    df_all.reset_index(drop=True, inplace=True)


    sanity_check_list = list(df_all["sanity_check"])
   
    print(len(otb_files_anno))
    Precision = np.array(Precision_test_avg) / len(otb_files_anno)
    NPrecision = np.array(NPrecision_test_avg) / len(otb_files_anno)
    Success = np.array(Success_test_avg) / len(otb_files_anno)

    Sanity_check_Average = np.mean(sanity_check_list)*100
    Success_Average = np.trapz(Success, x=Success_X)*100
    Precision_Average = np.trapz(Precision, x=Success_X)*100
    NPrecision_Average = np.trapz(NPrecision, x=Success_X)*100


    return Sanity_check_Average, Success_Average, Precision_Average, NPrecision_Average



import argparse


if __name__ == "__main__": 
    p = argparse.ArgumentParser(description='Get metrics from GT and submission')
    p.add_argument('--GT_zip', type=str, default='dummy_GT.zip',
        help='zipped folder with GT OTB tracking bounding boxes.')
    p.add_argument('--subm_zip', type=str, default='dummy_subm.zip',
        help='zipped folder with submitted OTB tracking bounding boxes.')

    args = p.parse_args()

    Coverage, Success, Precision, Normalized_Precision = evaluate(args.GT_zip, args.subm_zip)

    print("Coverage", Coverage)
    print("Precision", Precision)
    print("Normalized Precision", Normalized_Precision)
    print("Success", Success)

