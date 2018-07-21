from flask import Flask, render_template
from flask_socketio import SocketIO
import requests
import firebase
import json

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def simulator():
    cars = get_most_recent_cars()
    return render_template('simulator.html', data = cars)

def get_most_recent_cars():
    cars = {}
    all_history = firebase.get('/history', None)

    # Get all from prev_station, group by car_id and then get the most recent timestamp for each car

    for key, value in all_history.items():
        if value["station_id"] == PREV_STATION:
            try:
                if cars[value["car_id"]] and cars[value["car_id"]]["timestamp"] < value["timestamp"]:
                    # Same car_id but newer data
                    cars[value["car_id"]] = value
            except:
                cars[value["car_id"]] = value

    for key, value in cars.items():
        print (key, value)

    return cars

if __name__ == '__main__':
    PREV_STATION = 1
    MY_STATION_ID = 2
    firebase = firebase.FirebaseApplication('https://metronome-nyc.firebaseio.com', None)
    socketio.run(app)
