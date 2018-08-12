import os
from tqdm import tqdm
import zipfile
import argparse
import shutil


def main(trackingnet_dir="TrackingNet", overwrite_frames=False, chunks=[]):

	for chunk_folder in chunks:
		chunk_folder = chunk_folder.upper()
		zip_folder = os.path.join(trackingnet_dir, chunk_folder, "zips")

		if( os.path.exists(zip_folder)):

			for zip_file in tqdm(os.listdir(zip_folder), desc=chunk_folder):
				if (zip_file.endswith('.zip')):

					frame_folder = os.path.join(trackingnet_dir, chunk_folder, "frames", os.path.splitext(zip_file)[0])

					try:
						with zipfile.ZipFile(os.path.join(zip_folder, zip_file)) as zip_ref:
							
							# create frame folder if does not exist already
							if (os.path.exists(frame_folder)):

								# Check if there is the same number of files within the folder
								same_number_files = len(zip_ref.infolist()) == len(os.listdir(frame_folder))
															
								if (overwrite_frames or not same_number_files):
									shutil.rmtree(frame_folder)
									print("overwriting", frame_folder, "due to different number of file in the folder.")
									os.makedirs(frame_folder)

							# if frame folder does not exist, jsut create it
							else:	
								same_number_files = False				
								os.makedirs(frame_folder)

							# extract zip if necessary
							if(overwrite_frames or not same_number_files):
								zip_ref.extractall(os.path.join(frame_folder))

							# check that all the files were extracted
							same_number_files = len(zip_ref.infolist()) == len(os.listdir(frame_folder))
							if (not same_number_files):
								print("Warning:", frame_folder, "was not well extracted")


					except zipfile.BadZipFile:
						print("Error: the zip file", zip_file, "is corrupted, please delete it and download it again.")
						



if __name__ == "__main__": 
	p = argparse.ArgumentParser(description='Extract the frames for TrackingNet')
	p.add_argument('--trackingnet_dir', type=str, default='TrackingNet',
		help='Main TrackingNet folder.')
	p.add_argument('--overwrite_frames', action='store_true',
		help='Folder where to store the frames.')
	p.add_argument('--chunk', type=str, default="ALL",
		help='List of chunks to elaborate [ALL / Train / Test / 4 / 1,2,5].')

	args = p.parse_args()

	try:		
		if ("ALL" in args.chunk.upper()):
			chunk = ["TRAIN_"+str(c) for c in range(12)]
			chunk.insert(0, "TEST")		
		elif ("TEST" in args.chunk.upper()):
			chunk = ["TEST"]
		elif ("TRAIN" in args.chunk.upper()):
			chunk = ["TRAIN_"+str(c) for c in range(12)]
		else :
			chunk = ["TRAIN_"+str(int(c)) for c in args.chunk.split(",")]		
	except:		
		chunk = []


	print("extracting the frames for the following chunks:")
	print(chunk)

	main(args.trackingnet_dir, args.overwrite_frames, chunk)


