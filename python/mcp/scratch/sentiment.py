from transformers import pipeline

# create pipeline for sentiment analysis
classification = pipeline('sentiment-analysis')
response = classification('This is the best day ever!')
print(response)
