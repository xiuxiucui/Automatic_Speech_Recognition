
import requests
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import pandas as pd

host="http://ec2-13-212-254-81.ap-southeast-1.compute.amazonaws.com:9200"

es = Elasticsearch(host)

df=pd.read_csv(r'../asr/cv-valid-dev.csv')
df.fillna('N/A', inplace=True)
df_data=df.values.tolist()
def gendata(df_data):
    for data in df_data:
        yield {
            "_index": "cv-transcriptions",
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
