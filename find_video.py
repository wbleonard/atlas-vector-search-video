from sentence_transformers import SentenceTransformer
import params
from pymongo import MongoClient
import argparse

# Process arguments
parser = argparse.ArgumentParser(description='Atlas Vector Search Video Demo')
parser.add_argument('-q', '--query', help="The video content you're looking for")
args = parser.parse_args()

if args.query is None:
    # Some queries to try...
    query = "Flowers"
    
else:
    query = args.query

# Show the default query if one wasn't provided:
if args.query is None:
    print("\nYour query:")
    print("-----------")
    print(query)

# https://huggingface.co/sentence-transformers/clip-ViT-L-14
preTrainedModelName = "clip-ViT-L-14"
model = SentenceTransformer(preTrainedModelName)

# Encode our query
query_vector = model.encode(query).tolist()

# Establish connections to MongoDB
mongo_client = MongoClient(params.mongodb_conn_string)
result_collection = mongo_client[params.database][params.collection]

desired_answers = 3

pipeline = [
    {
        "$search": {
            "knnBeta": {
                "vector": query_vector,
                "path": "frameVector",
                "k": 15
            }
        }
    },
    {
        "$limit": desired_answers
    }
]

results = result_collection.aggregate(pipeline)

print("\nThe following videos may contain relevant content:")
print("--------------------------------------------------")

for result in results:

    print("video:     ", result['videoFile'])
    print("Second:    ", result['second']), "\n)"
    print("Frame:     ", result['frame'], "\n")