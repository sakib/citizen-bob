import json
import os
import time

from flask import Flask, request
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


app = Flask(__name__)

sg_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
subscribers = ['sagnewshreds@gmail.com', 'sakib.jalal@mongodb.com', 'drudolph914@gmail.com', 'sandile.keswa@gmail.com']


def world_to_map(world_x: int, world_y: int):
    world_ranges = {
        'lumbridge': {
            'world_coords': [(2000, 2000),(5000, 5000)],
            'map_coords': [400, 400]
        },
    }

    for town, info in world_coords.items():
        world_coords = info['world_coords']
        top_left = world_coords[0]
        bottom_right = world_coords[1]

        is_in_town = world_x >= top_left[0] \
            and world_x <= bottom_right[0] \
            and world_y >= top_left[1] \
            and world_y <= bottom_right[1]

        if is_in_town:
            return info['map_coords']


class CrimeReport:
    def __init__(self, username, crime, time, x_location, y_location):
        self.username = username
        self.crime = crime
        self.time = time
        self.x_location = x_location
        self.y_location = y_location

    def __repr__(self):
        return f'{self.username} has been spotted doing the following: {self.crime} at ({self.x_location}, {self.y_location}) at {self.time}'


app = Flask(__name__)
sg_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
subscribers = ['sagnewshreds@gmail.com', 'sakib.jalal@mongodb.com', 'drudolph914@gmail.com', 'sandile.keswa@gmail.com']
# Scalable highly-efficient in-memory data store to record all alerts
database = []
# minutes
CRIMINAL_ACTIVITY_RECENCY_ALGORITHM_HYPER_PARAMETER = 15
TIME_FORMAT = '%H:%M:%S'


with open('subscribers.txt') as file:
    for line in file:
        subscribers.append(line)


# these should be timestamps
def is_within_15_minutes(time1, time2):
    # Calculate the time difference
    time_diff = abs(time1_obj - time2_obj)

    # Check if the time difference is within TOLERABLE PARAMETERS
    return time_diff <= 60 * CRIMINAL_ACTIVITY_RECENCY_ALGORITHM_HYPER_PARAMETER


def string_to_unix_timestamp(date_string):
    # Parse the string into a datetime object
    date_obj = datetime.strptime(date_string, '%A, %B %d, %Y %H:%M:%S %p')

    # Convert the datetime object to a Unix timestamp
    unix_timestamp = date_obj.timestamp()

    # Convert to integer
    return int(unix_timestamp)


def nearby_ish(location1, location2):
    x1, y1 = location1
    x2, y2 = location2
    return abs(x1 - x2) < 100000 and abs(y1 - y2) < 100000


@app.route('/subscribe', methods=['POST'])
def subscribe():
    from_email = request.values.get('from')
    subscribers.add(from_email)
    return '', 200


@app.route('/report', methods=['POST'])
def blast():
    # location = json.loads(request.values.get('location'))
    report = CrimeReport(
        username = request.values.get('username'),
        crime = request.values.get('crime'),
        time = request.values.get('time'),
        x_location = request.values.get('x'),
        y_location = request.values.get('y'),
    )
    database.append(report)
    
    for email in subscribers:
        send_email('narc@sagnew.com', email, 'RUNESCAPE CRIME ALERT!', str(report))

    return '', 200


@app.route('/getcrimes', methods=['GET'])
def get_crimes():
    recent_crimes = []
    x = request.args.get('x')
    y = request.args.get('y')
    now = int(time.time())
    # for crime in database:
    #     crime_time = string_to_unix_timestamp(crime.time)
    #     if is_within_15_minutes(now, crime_time) and nearby_ish((x, y), (crime.x_location, crime.y_location)):
    #         recent_crimes.append(str(crime))
    # return recent_crimes
    return [str(crime) for crime in database]


def send_email(from_email, to_email, subject, body):
    message = Mail(from_email,
                 to_email,
                 subject,
                 body)
    response = sg_client.send(message)
    print(response.headers)


if __name__ == '__main__':
    app.run(debug=True, port=6000)
