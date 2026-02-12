from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# ================== Scheduling Algorithms ==================

def fcfs(processes):
    """First Come First Served"""
    processes = sorted(processes, key=lambda x: x['arrival'])
    time_line = 0
    result, gantt = [], []
    for process in processes:
        pid, at, bt = process['pid'], process['arrival'], process['burst']
        if time_line < at: time_line = at
        start = time_line
        finish = start + bt
        wt = start - at
        tat = finish - at
        result.append({'pid': pid, 'wt': wt, 'tat': tat})
        gantt.append({'pid': pid, 'start': start, 'finish': finish})
        time_line = finish
    return result, gantt

def sjf(processes):
    """Shortest Job First (Non-Preemptive)"""
    processes = sorted(processes, key=lambda x: (x['arrival'], x['burst']))
    return fcfs(processes)

def sjf_preemptive(processes):
    """Shortest Job First (Preemptive)"""
    time_line = 0
    remaining = {p['pid']: p['burst'] for p in processes}
    arrival = {p['pid']: p['arrival'] for p in processes}
    completed = {}
    gantt = []
    
    while len(completed) < len(processes):
        available = [p['pid'] for p in processes if arrival[p['pid']] <= time_line and p['pid'] not in completed]
        if available:
            pid = min(available, key=lambda x: remaining[x])
            gantt.append({'pid': pid, 'start': time_line, 'finish': time_line+1})
            remaining[pid] -= 1
            time_line += 1
            if remaining[pid] == 0: completed[pid] = time_line
        else:
            time_line += 1
    
    result = []
    for process in processes:
        pid, at, bt = process['pid'], process['arrival'], process['burst']
        tat = completed[pid] - at
        wt = tat - bt
        result.append({'pid': pid, 'wt': wt, 'tat': tat})
    return result, gantt

def round_robin(processes, quantum):
    """Round Robin Scheduling"""
    queue = []
    time_line = 0
    remaining = {p['pid']: p['burst'] for p in processes}
    arrival = {p['pid']: p['arrival'] for p in processes}
    completed = {}
    gantt = []
    
    processes = sorted(processes, key=lambda x: x['arrival'])
    i = 0
    
    while len(completed) < len(processes):
        while i < len(processes) and processes[i]['arrival'] <= time_line:
            queue.append(processes[i]['pid'])
            i += 1
        
        if queue:
            pid = queue.pop(0)
            exec_time = min(quantum, remaining[pid])
            gantt.append({'pid': pid, 'start': time_line, 'finish': time_line+exec_time})
            time_line += exec_time
            remaining[pid] -= exec_time
            while i < len(processes) and processes[i]['arrival'] <= time_line:
                queue.append(processes[i]['pid'])
                i += 1
            if remaining[pid] > 0:
                queue.append(pid)
            else:
                completed[pid] = time_line
        else:
            time_line += 1
    
    result = []
    for process in processes:
        pid, at, bt = process['pid'], process['arrival'], process['burst']
        tat = completed[pid] - at
        wt = tat - bt
        result.append({'pid': pid, 'wt': wt, 'tat': tat})
    
    return result, gantt

def priority_scheduling(processes):
    """Priority Scheduling (Non-Preemptive)"""
    processes = sorted(processes, key=lambda x: (x['arrival'], x.get('priority', 0)))
    time_line = 0
    result, gantt = [], []
    for process in processes:
        pid, at, bt = process['pid'], process['arrival'], process['burst']
        if time_line < at: time_line = at
        start = time_line
        finish = start + bt
        wt = start - at
        tat = finish - at
        result.append({'pid': pid, 'wt': wt, 'tat': tat})
        gantt.append({'pid': pid, 'start': start, 'finish': finish})
        time_line = finish
    return result, gantt

# ================== Flask Routes ==================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.json
    processes = data.get('processes', [])
    algorithm = data.get('algorithm', 'FCFS')
    quantum = data.get('quantum', 2)
    
    try:
        if algorithm == 'FCFS':
            result, gantt = fcfs(processes)
        elif algorithm == 'SJF':
            result, gantt = sjf(processes)
        elif algorithm == 'SJF_Preemptive':
            result, gantt = sjf_preemptive(processes)
        elif algorithm == 'RoundRobin':
            result, gantt = round_robin(processes, int(quantum))
        elif algorithm == 'Priority':
            result, gantt = priority_scheduling(processes)
        else:
            return jsonify({'error': 'Invalid algorithm'}), 400
        
        # Calculate statistics
        total_wt = sum(r['wt'] for r in result)
        total_tat = sum(r['tat'] for r in result)
        total_burst = sum(p['burst'] for p in processes)
        
        avg_wt = total_wt / len(result) if result else 0
        avg_tat = total_tat / len(result) if result else 0
        cpu_util = (total_burst / gantt[-1]['finish']) * 100 if gantt else 0
        throughput = len(processes) / gantt[-1]['finish'] if gantt else 0
        
        return jsonify({
            'result': result,
            'gantt': gantt,
            'statistics': {
                'avg_wt': round(avg_wt, 2),
                'avg_tat': round(avg_tat, 2),
                'cpu_util': round(cpu_util, 2),
                'throughput': round(throughput, 3)
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

