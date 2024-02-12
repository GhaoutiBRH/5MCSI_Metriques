from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3

                                                                                                                                       
app = Flask(__name__)
def get_commit_data():
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    try:
        with urlopen(url) as response:
            data = response.read().decode('utf-8')
            return json.loads(data)
    except urllib.error.HTTPError as e:
        # Gérer les erreurs si la requête échoue
        print(f"Erreur: Impossible de récupérer les données sur les commits (code {e.code})")
        return None

@app.route('/commits/')
def show_commit_counts():
    # Extract commit data from GitHub API
    commits_data = get_commit_data()
    if not commits_data:
        return "Impossible de récupérer les données sur les commits."

    # Process commit data to count commits per minute
    commits_per_minute = {}
    for commit in commits_data:
        commit_date = commit['commit']['author']['date']
        minute = extract_minutes(commit_date)
        commits_per_minute[minute] = commits_per_minute.get(minute, 0) + 1

    # Format the commit counts per minute as text
    commit_counts_text = "\n".join([f"{minute}: {count}" for minute, count in commits_per_minute.items()])

    return render_template('commit_counts.html', commit_counts_text=commit_counts_text)

# Helper function to extract minutes from date string
def extract_minutes(date_string):
    from datetime import datetime
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
