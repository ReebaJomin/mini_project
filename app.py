from flask import Flask, request, jsonify, render_template
import pandas as pd
import sqlite3

app = Flask(__name__)

#Load the CSV data into the database (one-time setup)
def load_csv_to_db():
    csv_file_path = r'C:\Users\DELL\Desktop\mini\Final_dataset.csv'
    df = pd.read_csv(csv_file_path)
    conn = sqlite3.connect('youtube_videos.db')
    df.to_sql('videos', conn, if_exists='replace', index=False)
    conn.close()

#Ensure the database is loaded
load_csv_to_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_videos', methods=['POST'])
def get_videos():
    data = request.json
    paragraph = data['A dog saves the life of the master from danger. One can find dogs everywhere in the world. It also has many qualities like swimming in the water, jumping from anywhere, good smelling sense. Dogs are sometimes called canines. Dogs are sometimes referred to as man’s best friend because they are kept as domestic pets and are usually loyal and like being around humans. The dogs are so loyal to his master that nothing can induce him to leave his master. His master might be a poor man or even a beggar but still, the dog will not leave his master from far off. Dogs see their master coming home from work they rush to them and jump on them to show their love. Dogs are honest friends who are always ready to die to save a friend. Dogs always give security to the owner day and night.']

    words = set(paragraph.lower().split())
    query = "SELECT title, url FROM videos WHERE " + " OR ".join([f"title LIKE '%{word}%'" for word in words])

    conn = sqlite3.connect('youtube_videos.db')
    c = conn.cursor()
    c.execute(query)
    matching_videos = c.fetchall()
    conn.close()

    return jsonify(matching_videos)

if __name__ == '__main':
    app.run(debug=True)