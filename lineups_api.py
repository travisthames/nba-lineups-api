from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/lineups", methods=["GET"])
def get_lineups():
    url = "https://www.rotowire.com/basketball/nba-lineups.php"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    matchups = []

    for matchup in soup.select(".lineup"):
        teams = matchup.select(".lineup__abbr")
        statuses = matchup.select(".lineup__status")
        starters = matchup.select(".lineup__players .lineup__player")

        if len(teams) == 2 and starters:
            away_team = teams[0].text.strip()
            home_team = teams[1].text.strip()
            game_status = statuses[0].text.strip() if statuses else "TBD"

            starter_names = [player.text.strip() for player in starters]
            matchups.append({
                "away_team": away_team,
                "home_team": home_team,
                "status": game_status,
                "starters": starter_names
            })

    return jsonify(matchups)

if __name__ == "__main__":
    app.run(debug=True)
