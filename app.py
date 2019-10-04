from flask import Flask, render_template, session, url_for, request, redirect, escape
from datetime import datetime
import os

app = Flask(__name__)

app.secret_key = os.urandom(16)
#app.config['SECRET KEY'] = "leyndo"

vorur = [
    [0, "Heyrnatól", "heyrnatol.jpg", 8500],
    [1, "Mús", "mus.jpg", 3000],
    [2, "Úr", "ur.jpg", 4500],
    [3, "Ryksuga", "ryksuga.jpg", 19000],
    [4, "Myndavel", "myndavel.jpg", 200000],
    [5, "Sjónvarp", "sjonvarp.jpg", 720000],
    [6, "Rakatæki", "rakataeki.jpg", 6000],
    [7, "Iphone 11", "iphone.jpg", 250000],
    [8, "Minnislykill", "lykill.jpg", 10000],
    [9, "Sous vide", "sous.jpg", 25000],
    [10, "Nokia 3310", "nokia.jpg", 10000]
]

@app.route("/")
def home():
    karfa = []
    fjoldi = 0
    if "karfa" in session:
        karfa = session["karfa"]
        fjoldi = len(karfa)
    return render_template('index.html', vorur=vorur, fjoldi=fjoldi)

@app.route("/add/<int:id>")
#idk man
def add(id):
    karfa = []
    if "karfa" in session:
        karfa = session["karfa"]
        karfa.append(vorur[id])
        session["karfa"] = karfa
        fjoldi = len(karfa)
    
    else:
        karfa.append(vorur[id])
        session["karfa"] = karfa
        fjoldi = len(karfa)

    return redirect(url_for("home"))
    #return render_template("index.html", vorur = vorur, fjoldi = fjoldi)

@app.route("/karfa")
def karfa():
    karfa = []
    summa = 0

    if 'karfa' in session:
        karfa = session["karfa"]
        fjoldi = len(karfa)
        for i in karfa:
            summa+=int(i[3])
        return render_template("karfa.html", karfa = karfa, tom = False, fjoldi = fjoldi, total=summa)
    else:
        return render_template("karfa.html", karfa=karfa, tom=True, fjoldi=0)

@app.route("/eyda")
def eyda():
    session.pop("karfa", None)
    return render_template("eyda.html", fjoldi=0)

@app.route("/eyda/<int:id>")
def eydahlut(id):
    karfa = []
    karfa = session["karfa"]
    index = 0
    for i in range(len(karfa)):
        if karfa[i][0] == id:
            index = i
    karfa.pop(index)
    session["karfa"] = karfa
    return redirect()

@app.route("/result", methods=["post"])
def result():
    if request.method == "POST":
        kwargs={
            "name":request.form["nafn"],
            "email":request.form["email"],
            "heimili":request.form["heimili"],
            "phone":request.form["simi"],
            "price":request.form["samtals"]
        }
        eyda()
        return render_template("result.html", **kwargs, fjoldi=0)

@app.errorhandler(404)
def pagenotfound(error):
    return render_template('pagenotfound.html')


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
    #app.run()