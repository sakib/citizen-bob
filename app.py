import os

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


with open('subscribers.txt') as file:
    for line in file:
        subscribers.append(line)


@app.route('/subscribe', methods=['POST'])
def subscribe():
    from_email = request.values.get('from')
    subscribers.add(from_email)
    return '', 200


@app.route('/report', methods=['POST'])
def blast():
    username = request.values.get('username')
    crime = request.values.get('crime')
    time = request.values.get('time')
    location = request.values.get('location')

    body = f'{username} has been spotted doing the following: {crime} at {location} at {time}'

    for email in subscribers:
        send_email('narc@sagnew.com', email, 'RUNESCAPE CRIME ALERT!', body)

    return '', 200


def send_email(from_email, to_email, subject, body):
    message = Mail(from_email,
                 to_email,
                 subject,
                 body)
    response = sg_client.send(message)
    print(response.headers)


if __name__ == '__main__':
    app.run(debug=True, port=6000)
