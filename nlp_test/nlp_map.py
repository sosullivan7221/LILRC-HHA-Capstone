import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import csv

mapping_file = 'nlp_test\job_mapping.csv'
job_mapping = {}

with open(mapping_file, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        standardized_title = row['standardized_title']
        survey_response_title = row['survey_response_title'].title()
        job_mapping[survey_response_title] = standardized_title
        
clean_csv_file = 'nlp_test\clean.csv'
df = pd.read_csv(clean_csv_file)

tfidf_vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
classifier = LogisticRegression(max_iter=1000)

pipeline = Pipeline([('tfidf', tfidf_vectorizer),
                     ('clf', classifier)])

X_train = list(job_mapping.keys())
y_train = list(job_mapping.values())

pipeline.fit(X_train, y_train)

X_test = df['Job Title'].tolist()
predicted_titles = pipeline.predict(X_test)

mask = df['Standard Titles'].isnull()
df.loc[mask, 'Standard Titles'] = predicted_titles[mask]

output_csv_file = 'final.csv'
df.to_csv(output_csv_file, index=False, encoding='utf-8')