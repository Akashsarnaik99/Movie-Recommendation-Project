from flask import Flask, render_template, request, jsonify
import pickle

model = pickle.load(open('models/similar.pkl',"rb"))

movie_list= pickle.load(open('models/bollywood_movies.pkl',"rb"))

app = Flask(__name__)
# @app.route("/")
# def home():
#     return render_template("index.html")

@app.route('/')
def index():

    movies = movie_list['original_title'].tolist()
    return render_template('index.html', movies_list=movies)



def recommend(name):
        index=movie_list[movie_list['original_title']==name].index[0]
        distance=sorted(list(enumerate(model[index])),reverse=True, key= lambda vector : vector[1])
        recommend_movies=[]
        poster_path=[]
        rating=[]

        for i in distance[1:9]:
            recommend_movies.append(movie_list.iloc[i[0]].original_title)
            poster_path.append(movie_list.iloc[i[0]].poster_path)
            rating.append(movie_list.iloc[i[0]].imdb_rating)

        return recommend_movies,poster_path,rating
@app.route('/get_name',methods=['GET','POST'])
def get_name():
    movies = movie_list['original_title'].tolist()
    name= request.form.get('movie_name')
    recommended_list, poster,rating = recommend(name)
    movie_poster_zip = zip(recommended_list, poster,rating)

    return render_template('index.html', movie_name=name, recommended_list=recommended_list, poster=poster,movie_poster_zip=movie_poster_zip, movies_list=movies)
    
   


if __name__ == "__main__":
    app.run(debug=True)