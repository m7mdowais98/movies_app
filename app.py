import logging
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Default credentials
USERNAME = "admin"
PASSWORD = "admin"

# In-memory movie list
movie_list = ["Inception", "The Matrix", "Interstellar", "The Dark Knight", "Pulp Fiction"]

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('movies'))
        else:
            app.logger.error("Invalid username or password")
            return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

@app.route('/movies', methods=['GET', 'POST'])
def movies():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        new_movie = request.form['new_movie']
        if new_movie:
            movie_list.append(new_movie)
    return render_template('movies.html', movies=movie_list)

@app.route('/remove_movie/<movie>', methods=['POST'])
def remove_movie(movie):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if movie in movie_list:
        movie_list.remove(movie)
    return redirect(url_for('movies'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
