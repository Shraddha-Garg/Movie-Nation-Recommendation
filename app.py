import streamlit as st
import pandas as pd
import difflib
import pickle
import requests
import time
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner


#declaring the header for our movie Recommendation web app
st.title('Movie Nation')

#basic function flow to incorporate lottie animations
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_url_movie = "https://assets10.lottiefiles.com/packages/lf20_CTaizi.json"
lottie_url_download = "https://assets4.lottiefiles.com/packages/lf20_IQ2L4E/download_from_cloud_05.json"
lottie_movie_json = load_lottieurl(lottie_url_movie)
lottie_download_json = load_lottieurl(lottie_url_download)
st_lottie(lottie_movie_json, key="hello", height=400, width=800)

#using pickle module to obtain datasets saved on disk in the form of pkl file
movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

#accepts users choice of movie and also displays a list of movies available
#using selectbox feature to help user select the movie
enter_movie_of_choice = st.selectbox(
'Search for a hollywood movie...',
movies['title'].values)

#list variable to obtain title of all movies present in database
movies_list = movies['title'].tolist()

#function that uses tmdb API to get (request) required movie posters
#from movie id passed as argument
def movie_Poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=67903b76645c49baf44bac83fac76700&language=en-US'.format(movie_id))
    information = response.json()
    return "https://image.tmdb.org/t/p/w500/" + information['poster_path']


#function to recommend movie
#it displays user entered movie at first
#besides also display other similar movie
def movie_Recommender(movie_name):

    #forms a list of all movie titles with a slight difference in spelling
    #using difflib module of Python
    list_of_close_match_titles = difflib.get_close_matches(movie_name, movies_list)
    first_match = list_of_close_match_titles[0]

    #calculating the index where movie name entered by user is present in our movies database
    index = movies[movies.title == first_match]['index'].values[0]

    #calculating the list of similarity difference between user's choice
    #and other movies in order to give best possible recomendations 
    calculated_similarity = list(enumerate(similarity[index]))
    
    #the calculated similarity scores of movie with respect to user's movie choice
    #is sorted in descending order using Python sorted() function
    #to display most relevant choice first
    sorted_calculated_similarity_list = sorted(calculated_similarity, key = lambda x : x[1], reverse = True)
    
    list_of_recommended_movies = []
    poster_of_recommended_movies = []

    #loop to calculate the list of first 12 recommended movie titles and their corresponding posters
    #using the earlier calculated index
    i = 1
    for movie_title in sorted_calculated_similarity_list:

        #here in command movie_title[0], subscript(index) is given as 0 
        #since sorted_calculated_similarity_list gives a tuple which has 2 values
        # first one being the index and second one is the calculated similarity score 
        index = movie_title[0]

        #using the index of different movies we obtain their titles and id from movies database
        title_from_index = movies[movies.index == index]['title'].values[0]
        id_from_index = movies[movies.index == index]['id'].values[0]

        #appending the first 12 movies and posters in their respective lists 
        if i < 13:
            list_of_recommended_movies.append(title_from_index)
            poster_of_recommended_movies.append(movie_Poster(id_from_index))
            i += 1
    return list_of_recommended_movies, poster_of_recommended_movies


if st.button('Recommend'):
    #displays animation till the time list of movies and poster is obtained
    with st_lottie_spinner(lottie_download_json, key="recommend", height=400, width=800):
      #function call to movie recommendation function
      recommended_movie_name, movie_posters = movie_Recommender(enter_movie_of_choice)
      time.sleep(2)
    st.balloons()

    #formed columns to display movie names along with their posters 
    col1, col2, col3 = st.columns(3)
    with col1:
      st.header(recommended_movie_name[0])
      st.image(movie_posters[0])
    with col2:
      st.header(recommended_movie_name[1])
      st.image(movie_posters[1])
    with col3:
      st.header(recommended_movie_name[2])
      st.image(movie_posters[2])
    with col1:
      st.header(recommended_movie_name[3])
      st.image(movie_posters[3])
    with col2:
      st.header(recommended_movie_name[4])
      st.image(movie_posters[4])
    with col3:
      st.header(recommended_movie_name[5])
      st.image(movie_posters[5])
    with col1:
      st.header(recommended_movie_name[6])
      st.image(movie_posters[6])
    with col2:
      st.header(recommended_movie_name[7])
      st.image(movie_posters[7])
    with col3:
      st.header(recommended_movie_name[8])
      st.image(movie_posters[8])
    with col1:
      st.header(recommended_movie_name[9])
      st.image(movie_posters[9])
    with col2:
      st.header(recommended_movie_name[10])
      st.image(movie_posters[10])
    with col3:
      st.header(recommended_movie_name[11])
      st.image(movie_posters[11])



