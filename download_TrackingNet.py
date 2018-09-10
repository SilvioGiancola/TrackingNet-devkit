import os
import pandas as pd
from tqdm import tqdm
import argparse

import downloader




def main(trackingnet_dir="TrackingNet", csv_dir=".", overwrite=False, chunks=[], data=["ANNO","ZIPS"]):

	for chunk_folder in chunks:
		chunk_folder = chunk_folder.upper()

		#if ("TEST" in chunk_folder):
		#	my_data = ["ZIPS"]
		#else:
		my_data = data


		for datum in my_data:


			data_folder = os.path.join(trackingnet_dir, chunk_folder, datum.lower())
			if(not os.path.exists(data_folder)):
				os.makedirs(data_folder)


			csv_file = os.path.join(csv_dir, chunk_folder + "_" + datum.upper() + ".csv")
			
			df = pd.read_csv(csv_file)
			for index, row in tqdm(df.iterrows(), desc="_".join([chunk_folder,datum]), total=len(df.index)):

				Google_drive_file_id = row["link"]
				Google_drive_file_name = row["name"]
				destination_path = os.path.join(trackingnet_dir, chunk_folder, datum.lower(), Google_drive_file_name)

				if (not os.path.exists(destination_path)): 

					downloader.download(url='https://drive.google.com/uc?id={id}'.format(id=Google_drive_file_id),
						output=destination_path,
						quiet=True,
					)



if __name__ == "__main__": 
	p = argparse.ArgumentParser(description='Download the frames for TrackingNet')
	p.add_argument('--trackingnet_dir', type=str, default='TrackingNet',
		help='Main TrackingNet folder.')
	p.add_argument('--overwrite', type=bool, default=False,
		help='Folder where to store the frames.')
	p.add_argument('--chunk', type=str, default="ALL",
		help='List of chunks to elaborate [ALL / Train / Test / 4 / 1,2,5].')
	p.add_argument('--data', type=str, default="ALL",
		help='Type of data [ALL / zips / anno / zips,anno].')
	p.add_argument('--csv_dir',    type=str, default='csv_link',
		help='Folder where the csv with the list of frames are. [default=csv_link]')

	args = p.parse_args()

	# type of data to download (zips/anno)
	try: 
		if ("ALL" in args.data.upper()):
			args.data = ["ANNO","ZIPS"]
		else:
			args.data = args.data.upper().split(",")  
	except:     
		args.data = []

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


	print("Downloading the data files for the following chunks")
	print("CHUNKS:", args.chunk)
	print("DATA:", args.data)

	main(trackingnet_dir=args.trackingnet_dir, 
		csv_dir=args.csv_dir, 
		overwrite=args.overwrite, 
		chunks=args.chunk, 
		data=args.data)


