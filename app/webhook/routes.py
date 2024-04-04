from flask import Blueprint, request, jsonify, render_template, json
from datetime import datetime
from bson import json_util
from app.extensions import app, collection

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')


# MongoDB Schema
def save_to_mongodb(request_id, author, action, from_branch, to_branch, timestamp):
    data = {
        'request_id': request_id,
        'author': author,
        'action': action,
        'from_branch': from_branch,
        'to_branch': to_branch,
        'timestamp': timestamp
    }
    collection.insert_one(data)


# @webhook.route('/', methods=['GET'])
# def home():
#     return jsonify({'message': 'Event data saved successfully'}), 200


@webhook.route('/receiver', methods=['POST'])
def github_webhook():
    try:
        data = request.json
        action = None
        from_branch = None
        to_branch = None
        request_id = None
        output = None
        author = None

        if "zen" in data:
            # It's a ping event
            return jsonify({'message': 'Ping event received'}), 200

        if "pull_request" in data:
            if data["pull_request"]["merged"]:
                # It's a merged pull request
                request_id = data["pull_request"]["id"]
                author = data["pull_request"]["merged_by"]["login"]
                from_branch = data["pull_request"]["head"]["ref"]
                to_branch = data["pull_request"]["base"]["ref"]
                timestamp = data["pull_request"]["merged_at"]
                timestamp_dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
                timestamp_formatted = timestamp_dt.strftime("%d %b %Y - %I:%M %p %Z")
                action = "MERGE_REQUEST"
                output = f"{author} merged branch \"{from_branch}\" to \"{to_branch}\" on {timestamp_formatted}"
            else:
                # It's a regular pull request
                request_id = data["pull_request"]["id"]
                author = data["pull_request"]["user"]["login"]
                from_branch = data["pull_request"]["head"]["ref"]
                to_branch = data["pull_request"]["base"]["ref"]
                timestamp = data["pull_request"]["created_at"]
                timestamp_dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
                timestamp_formatted = timestamp_dt.strftime("%d %b %Y - %I:%M %p %Z")
                action = "PULL_REQUEST"
                output = f"{author} submitted a pull request from \"{from_branch}\" to \"{to_branch}\" on {timestamp_formatted}"

        elif "ref" in data:
            # It's a push event
            request_id = data["head_commit"]["id"]
            author = data["head_commit"]["author"]["name"]
            to_branch = data["ref"].split("/")[-1]
            timestamp = data["head_commit"]["timestamp"]
            timestamp_dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S%z")
            timestamp_formatted = timestamp_dt.strftime("%d %b %Y - %I:%M %p")
            action = "PUSH_REQUEST"
            output = f"{author} pushed to {to_branch} on {timestamp_formatted}"

        else:
            app.logger.error("Unknown event type. Payload: %s", data)
            return jsonify({'error': 'Unknown event type'}), 400

        # Store data into MongoDB
        save_to_mongodb(request_id, author, action, from_branch, to_branch, timestamp_formatted)

        return jsonify({'message': 'Event data saved successfully', 'output': output}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@webhook.route('/fetch_data', methods=['GET'])
def fetch_data():
    try:
        # Fetch data from MongoDB
        webhook_data = collection.find()
        # Convert MongoDB cursor to list of dictionaries
        data_list = list(webhook_data)

        return json.loads(json_util.dumps(data_list)), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@webhook.route('/', methods=['GET'])
def show_data():
    return render_template('github_log.html')
