from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
import matplotlib.pyplot as plt
from datetime import datetime
from urllib.request import urlopen
import sqlite3
import os
                                                                                                                                       
app = Flask(__name__)



# Chemin vers le répertoire où se trouve votre script Flask
directory = os.path.dirname(os.path.realpath(__file__))

# Chemin vers le répertoire 'static'
static_directory = os.path.join(directory, 'static')

# Création du répertoire 'static' s'il n'existe pas déjà
if not os.path.exists(static_directory):
    os.makedirs(static_directory)


@app.route('/commits/')
def show_commit_graph():
    # Extract commit data from GitHub API
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    with urllib.request.urlopen(url) as response:
        data = response.read().decode('utf-8')
        commits_data = json.loads(data)

    # Process commit data to count commits per minute
    commits_per_minute = {}
    for commit in commits_data:
        commit_date = commit['commit']['author']['date']
        minute = extract_minutes(commit_date)
        commits_per_minute[minute] = commits_per_minute.get(minute, 0) + 1

    # Create plot
    minutes = list(commits_per_minute.keys())
    commit_counts = list(commits_per_minute.values())

    plt.plot(minutes, commit_counts)
    plt.xlabel('Minute')
    plt.ylabel('Number of Commits')
    plt.title('Commits per Minute')
    plt.grid(True)
    plt.savefig('static/commit_graph.png')  # Save plot as a static image file
    plt.close()

    return render_template('commit_graph.html')

# Helper function to extract minutes from date string
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    return date_object.minute

@app.route("/contact/")
def MaPremiereAPI():
    return "<h2>Ma page de contact</h2>"

@app.route("/Contactformulaire/")
def MaPageDeContact():
    return render_template("Contact.html")
  
@app.route('/')
def hello_world():
    return render_template('hello.html') #Comm2
  
if __name__ == "__main__":
  app.run(debug=True)
