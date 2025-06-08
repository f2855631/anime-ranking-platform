from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/")
def home():
    page = request.args.get("page", default=1, type=int)
    url = f"https://api.jikan.moe/v4/anime?page={page}"
    response = requests.get(url)
    data = response.json()

    anime_list = []
    for item in data["data"]:
        title_japanese = item.get("title_japanese")
        if not title_japanese:
            continue

        anime = {
            "name": title_japanese,
            "image_url": item["images"]["jpg"]["image_url"]
        }
        anime_list.append(anime)

    # ✅ 每頁只保留 20 筆動畫，讓排版整齊（兩行 10 張卡片）
    anime_list = anime_list[:20]

    total_pages = data["pagination"]["last_visible_page"]
    return render_template("index.html", anime_list=anime_list, current_page=page, total_pages=total_pages)

if __name__ == "__main__":
    app.run(debug=True)