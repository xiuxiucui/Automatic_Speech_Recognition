
import requests
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import pandas as pd

# host="http://ec2-3-27-34-117.ap-southeast-2.compute.amazonaws.com:9200"
host="http://localhost:9200"
index="transcription"

es = Elasticsearch(host)

df=pd.read_csv(r'../asr/final.csv')
df.fillna('N/A', inplace=True)
df_data=df.values.tolist()
def gendata(df_data):
    for data in df_data:
        yield {
            "_index": "generated_text",
            "filename": data[0],
            "_id": data[0],
            "text":data[1],
            "up_votes":data[2],
            "down_votes":data[3],
            "age":data[4],
            "gender":data[5],
            "accent":data[6],
            "duration":data[7],
            "generated_text":data[8],
        }
bulk(es, gendata(df_data))

print("____________")

print("completed")