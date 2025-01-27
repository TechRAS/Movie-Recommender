# Importing the libraries
import pandas as pd
import numpy as np
import ast
# Reading Dataset
movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')
movies = movies.merge(credits,on='title') #Merging important categories of Credits dataset into Movies dataset
# Categories used for the model: genre, id, keywords, id, overview, cast, crew
movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']] # Getting the required categories together
movies.isnull().sum() # Finding missing data
movies.dropna(inplace=True) # Removing the movies with missing data
movies.duplicated().sum() # Checking for duplicate data
def convert(obj):  # Defining function to give temperary integer values to the string data values
    L = []         # Empty list for storing
    for i in ast.literal_eval(obj):
        L.append(i['name'])  # Appending converted values in the empty list
    return L    
movies['genres'] = movies['genres'].apply(convert) # Applying the function
movies['keywords'] = movies['keywords'].apply(convert) # Applying the function
def convert3(obj):    # Defining new function to get only first 3 main movie cast 
    L = []
    counter = 0
    for i in ast.literal_eval(obj):
        if counter != 3:
            L.append(i['name'])
            counter += 1
        else:
            break
    return L   
movies['cast'] = movies['cast'].apply(convert3)  # Applying the function
def fetch_director(obj):    # Defining another function to get only 1 important crew: Director
    L = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            L.append(i['name'])
            break
    return L   
movies['crew'] = movies['crew'].apply(fetch_director) # Applying the function
movies['overview'] = movies['overview'].apply(lambda x:x.split())  # Spliting the whole overview string into parts to get tags
# Removing any spaces between the below categories so that they can be converted into tags
movies['genres'] = movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast'] = movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew'] = movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])
# Combining all the tags together
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew'] 
NewMovies = movies[['movie_id','title','tags']] # Making a new variable for storing only the categories required
NewMovies['tags'] = NewMovies['tags'].apply(lambda x:" ".join(x)) # Giving spaces in between
NewMovies['tags'] = NewMovies['tags'].apply(lambda x:x.lower())
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(NewMovies['tags']).toarray()
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()
def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)
NewMovies['tags'] = NewMovies['tags'].apply(stem)
vectors = cv.fit_transform(NewMovies['tags']).toarray()
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vectors)
def recommend(movie):
    movie_index = NewMovies[NewMovies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True, key=lambda x:x[1])[0:6]
    for i in movies_list:
        print(NewMovies.iloc[i[0]].title)
import pickle
pickle.dump(NewMovies,open('Movies.pkl','wb'))
pickle.dump(similarity,open('similarity.pkl','wb'))