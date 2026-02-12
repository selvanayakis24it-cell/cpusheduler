# ⚙️ CPU Scheduling Simulator - Professional Edition

A stunning, modern web-based CPU scheduling simulator with Bootstrap, CSS animations, and interactive visualizations.

## ✨ Features

- **Beautiful Modern UI** with Bootstrap 5 and custom CSS
- **5 Scheduling Algorithms:**
  - First Come First Served (FCFS)
  - Shortest Job First (SJF)
  - SJF Preemptive (SRTF)
  - Round Robin (RR)
  - Priority Scheduling

- **Interactive Visualizations:**
  - Animated Gantt Chart
  - Performance Metrics Chart (Chart.js)
  - Real-time Statistics

- **Responsive Design** - Works on all devices
- **User-Friendly Interface** - Easy to use for everyone
- **Professional Animations** - Smooth transitions and effects

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app.py
```

### 3. Open in Browser

Navigate to: **http://localhost:5000**

## 📖 How to Use

1. **Enter Process Details:**
   - Process ID (P1, P2, etc.)
   - Arrival Time (when process arrives)
   - Burst Time (CPU time needed)

2. **Select Algorithm:**
   - Choose from dropdown menu
   - Set Time Quantum (for Round Robin)

3. **Run Simulation:**
   - Click "RUN SIMULATION" button
   - View results instantly!

4. **Analyze Results:**
   - Process metrics table
   - Gantt chart visualization
   - Performance statistics
   - Comparison chart

## 🎨 Technologies Used

- **Backend:** Python, Flask
- **Frontend:** HTML5, CSS3, JavaScript
- **Framework:** Bootstrap 5
- **Charts:** Chart.js
- **Icons:** Font Awesome
- **Fonts:** Google Fonts (Poppins)

## 📊 Algorithms Explained

### FCFS (First Come First Served)
Simple FIFO scheduling - processes are executed in arrival order.

### SJF (Shortest Job First)
Non-preemptive - shortest burst time executed first.

### SJF Preemptive (SRTF)
Preemptive version - switches to shorter remaining time.

### Round Robin
Time-sharing with configurable quantum - fair distribution.

### Priority Scheduling
Processes with lower priority numbers execute first.

## 🌟 Features Highlights

- ✅ Real-time validation
- ✅ Animated transitions
- ✅ Responsive design
- ✅ Sample data loading
- ✅ Dynamic process addition
- ✅ CPU utilization calculation
- ✅ Average WT and TAT metrics
- ✅ Beautiful color-coded charts

## 🎯 Perfect For

- Students learning OS concepts
- Teachers demonstrating scheduling
- Developers analyzing algorithms
- Anyone interested in CPU scheduling

## 📱 Browser Support

- Chrome ✅
- Firefox ✅
- Safari ✅
- Edge ✅
- Opera ✅

## 💡 Tips

- Use sample data to quickly test algorithms
- Compare different algorithms with same data
- Adjust time quantum in Round Robin for different results
- Hover over Gantt chart for process details

## 🤝 Contributing

Feel free to enhance and customize this simulator!

## 📄 License

Open source - free to use and modify.

---

**Enjoy scheduling! ⚙️✨**
