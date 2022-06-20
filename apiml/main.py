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

'''
    Base class for the API REST
'''
class Parameters(BaseModel):
    get_value: Optional[str] = None,
    post_value: Optional[str] = None,
    time_value: Optional[str] = None

'''
    Divides a string into 2-grams
'''
def get2Grams(payload_obj):
    
    payload = str(payload_obj)
    ngrams = []
    for i in range(0,len(payload)-2):
        ngrams.append(payload[i:i+2])
    return ngrams

app = FastAPI()


@app.post("/parameters/")
async def root (myParameters: Parameters):

    # Loading the tf-idf vectorizer information

    vectorizer = load('tfidf_vectorizer.joblib') 
    tfidf_vectorizer = TfidfVectorizer(tokenizer=get2Grams, vocabulary=vectorizer)

    if myParameters.post_value is not None:
        param = myParameters.post_value
    else:
        param = myParameters.get_value
    
    # Code for predict new entries

    payloads_tfidf = tfidf_vectorizer.fit_transform(np.array([param])) 

    poly = load('2grams.joblib') 
    poly_pred = poly.predict(payloads_tfidf)

    # Api rest response

    if poly_pred[0] == "LEGAL" :
        return "LEGAL"
    else:
        return poly_pred[0]

    return 