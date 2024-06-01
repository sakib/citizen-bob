import os

from flask import Flask, request
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


app = Flask(__name__)

sg_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
subscribers = ['sagnewshreds@gmail.com', 'sakib.jalal@mongodb.com', 'drudolph914@gmail.com', 'sandile.keswa@gmail.com']

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
