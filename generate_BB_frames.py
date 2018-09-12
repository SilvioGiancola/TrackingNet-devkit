import os
import pandas as pd
from tqdm import tqdm
import argparse

import downloader

import numpy as np

import cv2
	
def printBB(TrackingNet_dir, frames_folder, BB_file):

	ArrayBB = np.loadtxt(BB_file, delimiter=",")  

	frames_list=[os.path.join(TrackingNet_dir, frame) for frame in os.listdir(frames_folder) if frame.endswith(".jpg") ]
	frames_BB_folder = frames_folder.replace("frames", "frames_BB")


	if ( not len(ArrayBB) == len(frames_list)):
		#print("Not the same number of frames and annotation!" ) 
		if (np.ndim(ArrayBB) == 1):
			tmp = ArrayBB
			del ArrayBB
			ArrayBB = [[]]
			ArrayBB[0] = tmp


	if(not os.path.exists(frames_BB_folder)):
		os.makedirs(frames_BB_folder)



	if (len(os.listdir(frames_BB_folder)) == len(os.listdir(frames_folder))):
		# print("already Extracted") 
		return

	for i in range(len(ArrayBB)):

		frame_file = str(i)+".jpg"
		imgs_file = os.path.join(frames_folder, frame_file)
		imbb_file = os.path.join(frames_BB_folder, frame_file)

		frame = cv2.imread(imgs_file)
		height, width, channels = frame.shape 


		x_min = int(ArrayBB[i][0])
		x_max = int(ArrayBB[i][2] + ArrayBB[i][0])
		y_min = int(ArrayBB[i][1])
		y_max = int(ArrayBB[i][3] + ArrayBB[i][1])

		cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0,0,255), 2)
		cv2.imwrite(imbb_file, frame)




def main(output_dir="TrackingNet", overwrite=False, chunks=[]):

	for chunk_folder in chunks:
		chunk_folder = chunk_folder.upper()

		

		list_sequences = os.listdir(os.path.join(output_dir, chunk_folder, "frames"))

		for seq_ID in tqdm(list_sequences, desc=chunk_folder):

			frames_folder = os.path.join(output_dir, chunk_folder, "frames", seq_ID)
			BB_file = os.path.join(output_dir, chunk_folder, "anno", seq_ID + ".txt")
			printBB(output_dir, frames_folder=frames_folder, BB_file=BB_file)





if __name__ == "__main__": 
	p = argparse.ArgumentParser(description='Download the frames for TrackingNet')
	p.add_argument('--output_dir', type=str, default='TrackingNet',
		help='Main TrackingNet folder.')
	p.add_argument('--overwrite', type=bool, default=False,
		help='Folder where to store the frames.')
	p.add_argument('--chunk', type=str, default="ALL",
		help='List of chunks to elaborate [ALL / 4 / 1,2,5].')

	args = p.parse_args()


	# chunk of data to download (Test/Train_i)
	try:       
		if ("ALL" in args.chunk.upper()):
			args.chunk = ["TRAIN_"+str(c) for c in range(12)]
			args.chunk.insert(0, "TEST")     
		elif ("TEST" in args.chunk.upper()):
			args.chunk = ["TEST"]
		elif ("TRAIN" in args.chunk.upper()):
			args.chunk = ["TRAIN_"+str(c) for c in range(12)]
		else :
			args.chunk = ["TRAIN_"+str(int(c)) for c in args.chunk.split(",")]       
	except:     
		args.chunk = []


	print("Draw Bounding Boxes on the annotated frames for the following chunks")
	print("CHUNKS:", args.chunk)

	main(output_dir=args.output_dir, 
		overwrite=args.overwrite, 
		chunks=args.chunk)


