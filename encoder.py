from sentence_transformers import SentenceTransformer
from PIL import Image
from extract_frames import *
import params
from pymongo import MongoClient

# Extract frames from the videos
frames_dir = 'frames'
interval_secs = 2
extract_frames(frames_dir, interval_secs)

# Establish connections to MongoDB
mongo_client = MongoClient(params.mongodb_conn_string)
result_collection = mongo_client[params.database][params.collection]

# Empty the collection (Don't delete it to preserve the Search index)
result_collection.delete_many({})

#Load CLIP model
preTrainedModelName = "clip-ViT-L-14"
model = SentenceTransformer(preTrainedModelName)

frames_directory ="frames"

frames = [] 
for filename in os.listdir(frames_dir):
    filepath = os.path.join(frames_dir, filename)
    videoname = filename[0:filename.find('_sec')]
    videosec = int(filename[filename.find('_sec')+4: filename.find('_frame') ])
    videoframe = int(filename[filename.find('_frame')+6: filename.find('.jpg') ])
    frames.append({'filename': filename, 'filepath':filepath, 'videoname': videoname, 'videosec': videosec, 'videoframe': videoframe})

def vectorize(frames):
    print("\nVectorizng video frames...")
    for f in frames:
        if os.path.isfile(f['filepath']):
            encoded = model.encode(Image.open(f['filepath'])).tolist()
            image = {
                "videoFile": f['videoname'],
                "second": f['videosec'],
                "frame": f['videoframe'],       
                "imageVector": encoded
            }
            result_collection.insert_one(image)
            print(f['filename'])

vectorize(frames)

clean_up(frames_dir)

    