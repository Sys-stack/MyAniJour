from flask import Flask, render_template
import requests

app = Flask(__name__)

ANILIST_API_URL = "https://graphql.anilist.co"

def get_anime_data():
    query = """
    query {
      Page(page: 1, perPage: 10) {
        media(season: WINTER, seasonYear: 2025, type: ANIME) {
          title {
            romaji
            english
          }
          description
          coverImage {
            large
          }
          siteUrl
        }
      }
    }
    """
    response = requests.post(ANILIST_API_URL, json={"query": query})
    
    if response.status_code == 200:
        data = response.json()
        return data["data"]["Page"]["media"]
    else:
        return []

@app.route('/')
def home():
    anime_list = get_anime_data()
    html = requests.get("https://cdn.jsdelivr.net/gh/Sys-stack/MyAniJour@latest/Home.html").text
    return render_template(html, anime_list=anime_list)

if __name__ == '__main__':
    app.run(debug=True)
