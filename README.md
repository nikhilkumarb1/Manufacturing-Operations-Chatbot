

# 🚀 AI Chatbot for Manufacturing Plant Operations

A web-based AI chatbot that allows manufacturing plant staff to access **real-time production, maintenance, and downtime data** through simple natural language conversation — eliminating the need for complex software systems.

---

## 📌 **Project Overview**

Manufacturing supervisors often spend **15–30 minutes** navigating multiple systems just to retrieve basic operational data.
This project solves that problem by providing a **smart conversational interface** that responds instantly to queries like:

* “Show today’s production”
* “Which machines need maintenance?”
* “Why was Line 1 down yesterday?”

The chatbot fetches live data from the database and displays clean summaries, alerts, and visual charts.

---

## 🎯 **Features**

### 🤖 **Natural Language Query Support**

Ask questions in plain English — no technical knowledge required.

### 📊 **Real-Time Operational Data**

Live information about:

* Production
* Machine status
* Maintenance schedule
* Downtime and root causes

### 🚨 **Smart Alerts**

Automatic warnings when downtime exceeds set thresholds (e.g., > 30 minutes).

### 📈 **Visual Analytics**

Dynamic charts generated using **Matplotlib** to show trends for production, downtime, etc.

### 💡 **User-Friendly Interface**

Simple, clean web UI designed for non-technical factory staff.

---

## 🛠️ **Tech Stack**

| Component     | Technology                      |
| ------------- | ------------------------------- |
| Frontend      | HTML, CSS, JavaScript           |
| Backend       | Python Flask                    |
| Database      | MySQL                           |
| Visualization | Matplotlib                      |
| Logic         | Rule-based NLP & Intent Mapping |

---

## 🗂️ **Database Structure**

The system uses multiple tables such as:

* **Machines** (status, maintenance type)
* **Production Records** (units produced, shift, time)
* **Maintenance Schedule** (due-date, cost, remarks)
* **Downtime Logs** (machine, duration, cause)

Total sample data includes:

* 8 machines
* 60+ production entries
* Maintenance & downtime history

---

## ⚙️ **How It Works**

1. The user enters a natural language query.
2. Flask processes the query using simple NLP rules.
3. The intent is mapped to an SQL query.
4. MySQL retrieves the relevant data.
5. The response is formatted and sent back to the user.
6. If needed, charts are generated using Matplotlib and displayed.

---

---

## 🚧 **Challenges Faced**

### 1. Query Understanding

Mapping user language to SQL queries was difficult initially.
✔️ Solved using rule-based NLP keyword detection.

### 2. Database Design

Handling production, maintenance, and downtime in one schema.
✔️ Solved using normalized tables and foreign keys.

### 3. Real-Time Updating

Ensuring charts and summaries reflect live data.
✔️ Achieved through dynamic SQL queries and Matplotlib integration.

---

## 📌 **Future Enhancements**

* Machine Learning–based **predictive maintenance**
* IoT sensor data integration
* Mobile app version for shop-floor workers
* Multi-plant enterprise dashboard
* Voice-enabled chatbot

---

## ⭐ **Support**

If you like this project, consider giving it a ⭐ on GitHub!

---

MIT License

Copyright (c) 2025 Nikhil Kumar 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights  
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell      
copies of the Software, and to permit persons to whom the Software is         
furnished to do so, subject to the following conditions:                       

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.                                

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR     
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,       
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE    
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER         
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE  
SOFTWARE.

