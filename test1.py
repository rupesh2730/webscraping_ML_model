from app import *
import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Load the scraped data
csv_filename = "inner_data.csv"
data_df = pd.read_csv(csv_filename)

# Vectorize the text data
vectorizer = CountVectorizer()
X_vec = vectorizer.fit_transform(data_df['Statement'])

# Train the model
model = MultinomialNB()
model.fit(X_vec, data_df['Label'])

# Streamlit App
st.title(' Classification')

# User input for statement
user_input = st.text_area('Enter a statement for classification:')
if user_input:
    # Vectorize the user input
    user_input_vec = vectorizer.transform([user_input])

    # Make prediction
    prediction = model.predict(user_input_vec)

    # Display the result
    st.write(f'Predicted Label: {prediction[0]}')

# Display the scraped data
st.header('Scraped Data')
st.dataframe(data_df)
