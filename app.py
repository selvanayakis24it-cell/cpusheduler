from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# ============== SCHEDULING ALGORITHMS ==============

def fcfs(processes):
    """First Come First Served"""
    processes = sorted(processes, key=lambda x: x['arrival'])
    time = 0
    result = []
    gantt = []

    for p in processes:
        if time < p['arrival']:
            time = p['arrival']
        start = time
        finish = time + p['burst']
        wt = start - p['arrival']
        tat = finish - p['arrival']
        
        result.append({
            'pid': p['pid'],
            'wt': wt,
            'tat': tat
        })
        gantt.append({
            'pid': p['pid'],
            'start': start,
            'end': finish
        })
        time = finish

    return result, gantt

def solve_non_preemptive(processes, criteria_key):
    """Helper for non-preemptive scheduling (SJF, Priority)"""
    remaining = processes.copy()
    remaining.sort(key=lambda x: x['arrival']) # Sort by arrival for tie-breaking
    
    time = 0
    result = []
    gantt = []
    
    completed_count = 0
    n = len(remaining)
    
    # If first process arrives later than 0
    if remaining and remaining[0]['arrival'] > time:
        time = remaining[0]['arrival']

    while remaining:
        # Find candidates that have arrived
        candidates = [p for p in remaining if p['arrival'] <= time]
        
        if not candidates:
            # No process available, jump to next arrival
            if remaining:
                time = min(p['arrival'] for p in remaining)
                continue
            else:
                break
        
        # Select best candidate
        # criteria_key returns value to minimize
        p = min(candidates, key=criteria_key)
        
        remaining.remove(p)
        
        start = time
        finish = time + p['burst']
        wt = start - p['arrival']
        tat = finish - p['arrival']
        
        result.append({
            'pid': p['pid'],
            'wt': wt,
            'tat': tat
        })
        gantt.append({
            'pid': p['pid'],
            'start': start,
            'end': finish
        })
        
        time = finish
        
    return result, gantt

def sjf(processes):
    """Shortest Job First (Non-preemptive)"""
    # Min burst time, tie-break with arrival (handled by stable sort/min behavior if sorted by arrival first)
    return solve_non_preemptive(processes, lambda p: p['burst'])

def sjf_preemptive(processes):
    """Shortest Remaining Time First"""
    time = 0
    # Copy to avoid modifying original info
    remaining_burst = {p['pid']: p['burst'] for p in processes}
    processes_map = {p['pid']: p for p in processes}
    
    completed = []
    gantt = []
    
    # Total active processes
    incomplete_pids = set(p['pid'] for p in processes)
    
    # Pre-sort by arrival for efficiency in finding waiting jobs? 
    # Actually just iterate is simpler for simulation
    
    while incomplete_pids:
        # Available processes
        available = [pid for pid in incomplete_pids if processes_map[pid]['arrival'] <= time]
        
        if not available:
            # Jump time
            # Find closest next arrival
            future = [processes_map[pid]['arrival'] for pid in incomplete_pids if processes_map[pid]['arrival'] > time]
            if future:
                time = min(future)
            else:
                break # Should not happen
            continue

        # Select process with min remaining time
        pid = min(available, key=lambda x: remaining_burst[x])
        
        # Run for 1 unit
        gantt.append({
            'pid': pid,
            'start': time,
            'end': time + 1
        })
        
        remaining_burst[pid] -= 1
        time += 1
        
        if remaining_burst[pid] == 0:
            p = processes_map[pid]
            finish = time
            tat = finish - p['arrival']
            wt = tat - p['burst']
            completed.append({
                'pid': pid,
                'wt': wt,
                'tat': tat
            })
            incomplete_pids.remove(pid)
    
    # Merge contiguous gantt blocks
    if gantt:
        merged_gantt = []
        current = gantt[0].copy()
        for i in range(1, len(gantt)):
            next_block = gantt[i]
            if next_block['pid'] == current['pid'] and next_block['start'] == current['end']:
                current['end'] = next_block['end']
            else:
                merged_gantt.append(current)
                current = next_block.copy()
        merged_gantt.append(current)
        gantt = merged_gantt

    return completed, gantt

def round_robin(processes, quantum):
    """Round Robin Scheduling"""
    queue = []
    time = 0
    remaining_burst = {p['pid']: p['burst'] for p in processes}
    arrival_map = {p['pid']: p['arrival'] for p in processes}
    burst_map = {p['pid']: p['burst'] for p in processes}
    
    # Sort by arrival
    sorted_procs = sorted(processes, key=lambda x: x['arrival'])
    
    gantt = []
    completed = []
    
    added_to_queue = {p['pid']: False for p in processes}
    completed_pids = set()
    
    # Initial load of queue at time 0
    # Actually needs dynamic handling
    
    i = 0 # Index in sorted_procs
    
    # Handle the start time (if > 0)
    if sorted_procs and sorted_procs[0]['arrival'] > time:
        time = sorted_procs[0]['arrival']
        
    while len(completed) < len(processes):
        # Add newly arrived processes to queue
        while i < len(sorted_procs) and sorted_procs[i]['arrival'] <= time:
            if not added_to_queue[sorted_procs[i]['pid']]:
                queue.append(sorted_procs[i]['pid'])
                added_to_queue[sorted_procs[i]['pid']] = True
            i += 1
            
        if queue:
            pid = queue.pop(0)
            
            exec_time = min(quantum, remaining_burst[pid])
            
            gantt.append({
                'pid': pid,
                'start': time,
                'end': time + exec_time
            })
            
            time += exec_time
            remaining_burst[pid] -= exec_time
            
            # Check for new arrivals during this execution
            while i < len(sorted_procs) and sorted_procs[i]['arrival'] <= time:
                 if not added_to_queue[sorted_procs[i]['pid']]:
                    queue.append(sorted_procs[i]['pid'])
                    added_to_queue[sorted_procs[i]['pid']] = True
                 i += 1
            
            if remaining_burst[pid] > 0:
                queue.append(pid)
            else:
                p_arrival = arrival_map[pid]
                p_burst = burst_map[pid]
                tat = time - p_arrival
                wt = tat - p_burst
                completed.append({
                    'pid': pid,
                    'wt': wt,
                    'tat': tat
                })
        else:
            # Queue empty, jump to next arrival
            if i < len(sorted_procs):
                time = sorted_procs[i]['arrival']
            else:
                time += 1 # Should not happen unless finished
                
    return completed, gantt

def priority_scheduling(processes):
    """Priority Scheduling (Non-preemptive)"""
    # Lower value = Higher Priority? 
    # Usually in OS: depends. Unix: low num = high prio. Windows: high num = high prio.
    # The UI shows "1, 2, 3..." usually people assume 1 is first.
    # I'll stick to MIN value is HIGHEST priority (runs first).
    return solve_non_preemptive(processes, lambda p: p.get('priority', 0))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        data = request.json
        processes = data['processes']
        algorithm = data['algorithm']
        quantum = int(data.get('quantum', 2))
        
        # Run the selected algorithm
        if algorithm == 'FCFS':
            result, gantt = fcfs(processes)
        elif algorithm == 'SJF':
            result, gantt = sjf(processes)
        elif algorithm == 'SJF_Preemptive':
            result, gantt = sjf_preemptive(processes)
        elif algorithm == 'RoundRobin':
            result, gantt = round_robin(processes, quantum)
        elif algorithm == 'Priority':
            result, gantt = priority_scheduling(processes)
        else:
            return jsonify({'error': 'Invalid algorithm'}), 400
        
        # Calculate statistics
        total_wt = sum(r['wt'] for r in result)
        total_tat = sum(r['tat'] for r in result)
        avg_wt = total_wt / len(result)
        avg_tat = total_tat / len(result)
        
        total_burst = sum(p['burst'] for p in processes)
        total_time = gantt[-1]['end'] if gantt else 0
        cpu_util = (total_burst / total_time * 100) if total_time > 0 else 0
        
        return jsonify({
            'result': result,
            'gantt': gantt,
            'statistics': {
                'avg_wt': round(avg_wt, 2),
                'avg_tat': round(avg_tat, 2),
                'cpu_util': round(cpu_util, 2)
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
