from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.json
    processes = data['processes']

    result = []
    total_wt = 0
    total_tat = 0
    time = 0

    for p in processes:
        wt = max(0, time - p['arrival'])
        tat = wt + p['burst']
        time += p['burst']

        result.append({
            "pid": p['pid'],
            "wt": wt,
            "tat": tat
        })

        total_wt += wt
        total_tat += tat

    avg_wt = total_wt / len(processes)
    avg_tat = total_tat / len(processes)

    return jsonify({
        "result": result,
        "statistics": {
            "avg_wt": avg_wt,
            "avg_tat": avg_tat,
            "cpu_util": 100
        },
        "gantt": []
    })

if __name__ == '__main__':
    app.run(port=5000)