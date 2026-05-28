import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import joblib
import requests

def create_embedding(text_list):
    r = requests.post(
        "http://localhost:11434/api/embed",
        json={
            "model": "bge-m3",
            "input": text_list
        }
    )
    embeddings = r.json()['embeddings']
    return embeddings

def inference(prompt):
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream" : False
        }
    )
    response = r.json()
    print(response)
    return response


df = joblib.load('embeddings.joblib')
incoming_query = input("ask the ques : ")
question_query = create_embedding([incoming_query])[0]

#find the similarity question query with other query
# print(np.vstack(df['embedding'].values))
# print(np.vstack(df['embedding'].shape))

similarites = cosine_similarity(np.vstack(df['embedding']),[question_query]).flatten()
top_result = 5
max_indx = similarites.argsort()[::-1][0:top_result]
print(max_indx)
new_df = df.loc[max_indx]
#print(new_df[['title','number','text']])
prompt = f''' Iam teaching python in my python programming of course. Here are viedo subtitle chunks containing viedo title , viedo number , start time in sec,end time in sec,the text of that time.

{new_df[['title','number','start','end','text']].to_json(orient = "records")}
----------------------------------
"{incoming_query}"
user asked this question realted to the viedo chunk , you  have to answerin a human way(dont mention the above format its just for you) where and how much
content is taught where (in which viedo at what timestamp) and guide the user to go to that particular viedo.
If user asks unrelated question,tell him you can only answer questions related to course
'''

with open("prompt.txt","w")as f:
    f.write(prompt)

response = inference(prompt)['response']
print(response)

with open("response.txt" ,"w")as f:
    f.write(response)
# for index , item in new_df.iterrows():
#     print(index,item['title'],item['number'],item['text'],item['start'],item['end'])
