from flask import Flask, render_template, redirect, url_for, request
import create
import query

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("form.html")

@app.route('/results')
def results():
    if "rarity" in request.args:
        rarity = request.args.get("r", "Common")
        return render_template("results.html", query="Cards that are " + rarity, list=query.get_by_rarity(rarity))
    elif "cmc" in request.args:
        min = request.args.get("min", '0')
        max = request.args.get("max", '10')
        return render_template("results.html", query="Cards that cost between "+min+" and "+max+" mana", list=query.get_mana_range(min, max))
    else:
        return redirect(url_for("homepage"))

if __name__ == "__main__":
    create.makeDatabase()
    app.debug = True
    app.run()