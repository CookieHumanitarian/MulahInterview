from flask import Flask, jsonify
import csv

app = Flask(__name__)

@app.route('/rss-data')
def rss_data():
    data = []
    try:
        with open('rss_data.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
