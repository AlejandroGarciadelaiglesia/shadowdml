from typing import Optional
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn import svm
from sklearn import metrics
from sklearn.decomposition import PCA
from sklearn.decomposition import TruncatedSVD
from joblib import dump, load
import time


class Parameters(BaseModel):
    get_value: Optional[str] = None,
    post_value: Optional[str] = None,
    time_value: Optional[str] = None


def get2Grams(payload_obj):
    '''Divides a string into 2-grams
    
    Example: input - payload: "<script>"
             output- ["<s","sc","cr","ri","ip","pt","t>"]
    '''
    payload = str(payload_obj)
    ngrams = []
    for i in range(0,len(payload)-2):
        ngrams.append(payload[i:i+2])
    return ngrams

app = FastAPI()


@app.post("/parameters/")
async def root (myParameters: Parameters):

    if myParameters.time_value is not None:
        with open('times_waf.txt', 'a') as f:
            f.write(str(myParameters.time_value) + "\n")
        return

    vectorizer = load('tfidf_vectorizer.joblib') 
    tfidf_vectorizer = TfidfVectorizer(tokenizer=get2Grams, vocabulary=vectorizer)

    if myParameters.post_value is not None:
        param = myParameters.post_value
    else:
        param = myParameters.get_value
    
    payloads_tfidf = tfidf_vectorizer.fit_transform(np.array([param])) 

    poly = load('2grams.joblib') 
    poly_pred = poly.predict(payloads_tfidf)

    with open('result_ml.txt', 'a') as f:
        f.write(str(param) + "ç" + str(poly_pred[0]) + "\n")
    
    print(str(poly_pred[0]))

    if poly_pred[0] == "LEGAL" :
        return "LEGAL"
    else:
        return poly_pred[0]

    return 