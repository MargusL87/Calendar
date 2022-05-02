from flask import Flask, render_template, jsonify, request, url_for,redirect
#from edit_db import load_db, save_db, delete
from SQL_calls import load_db, append_db, move_db, update_db, delete_db

app = Flask(__name__)
app.run(use_reloader=False)

db = load_db()

@app.route("/")
def welcome():
    return render_template("new_index.html")

# funktio lähettää sivulle dataa db.jason tietostosta
@app.route("/eventlist")
def eventlist():
    global db
    test_json = jsonify(db)
    return test_json

# Tallentaa db.json tietostoon
@app.route("/add_event", methods=["POST"])
def add_event():
    global db
    if request.method == "POST":
        event = request.get_json()
        db.append(event)
        #save_db(db) # only with json
        append_db(event)
        return event

@app.route("/move_event", methods=["POST"])
def move_event():
    global db
    result = "NOT_OK"
    if request.method == "POST":
        event = request.get_json()
        id = event["id"]
        for i in range(len(db)):
            if db[i]["id"]==str(id):
                db[i]["start"] = event["newStart"]
                db[i]["end"] = event["newEnd"]
                #result = save_db(db) # only with json
                result = move_db(event)
                break
    return result

@app.route("/update_event", methods=["POST"])
def update_event():
    global db
    result = "NOT_OK"
    if request.method == "POST":
        event = request.get_json()
        for i in range(len(db)):
            if event["id"] == db[i]["id"]:
                db[i]["reg_nro"] = event["reg_nro"]
                db[i]["merkki"] = event["merkki"]
                db[i]["asiakas"] = event["asiakas"]
                db[i]["puh_nro"] = event["puh_nro"]
                db[i]["tyomaarays"] = event["tyomaarays"]
                #save_db(db) # only with json
                result = update_db(event)
                return event #should it return something else, if update fails?

# Poistaa tapahtuman db.json:sta. Key = id
@app.route("/delete_event", methods=["POST"])
def delete_event():
    global db
    result = "NOT_OK"
    if request.method == "POST":
        event = request.get_json()
        event_id = event["id"]
        for i in range(len(db)):
            if db[i]["id"]==event_id:
                del db[i]
                #save_db(db) only with json
                result = delete_db(event_id)
                break
    return result