# website/rasaweb/utils/learning_recommendation.py
# __author__='Lokesh Kuncham'

import pandas as pd
import neattext.functions as nfx

from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity,linear_kernel
def load_data(data):
    df = pd.read_csv(data)
    return df
df = load_data(r"C:\py\blog-master\blog-master\rasa\udemy_data\udemy_courses.csv")
import json

def search_based_on_intreset_domain(domain,interest,df=df):
    domain_df = df[df['subject']==domain]
    sorted_df = domain_df.sort_values(by=['num_subscribers'], ascending=False)
    filtered_df = sorted_df[sorted_df['course_title'].str.contains(interest,case=False)].head(3)
    filtered_res = filtered_df.to_dict()
    return filtered_res
