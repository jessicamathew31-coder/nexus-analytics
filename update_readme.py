readme = '''# 🚀 NEXUS ANALYTICS
### Live Financial Intelligence Dashboard

![Nexus Analytics Dashboard](dashboard.png)

> A production-grade interactive financial dashboard built from absolute zero using Python & Plotly Dash — analysing real Fortune 500 10-K annual report data spanning 14 years (2009–2023).

---

## 📌 Project Overview

NEXUS ANALYTICS is a fully deployed, interactive financial intelligence dashboard that visualises real corporate financial data from Fortune 500 companies. Built entirely using Python, this project demonstrates end-to-end data engineering — from raw dataset ingestion to a live, publicly accessible web application.

This is **Project 2** of my BSA (Business Systems Analyst) portfolio, designed to showcase technical capability in data visualisation, Python development, and cloud deployment.

🔗 Live Demo: https://nexus-analytics-272h.onrender.com
💻 GitHub: https://github.com/jessicamathew31-coder/nexus-analytics
👩 LinkedIn: https://linkedin.com/in/jessicasmathew

---

## ✨ Features

| Feature | Description |
|---|---|
| 📊 KPI Cards | Total Revenue, Avg Net Income, Avg ROE, Avg Market Cap |
| 📈 Trend Analysis | Revenue vs Net Income trend (2009-2023) |
| 🏆 Rankings | Top 10 companies by Market Cap |
| 🔍 Scatter Analysis | ROE vs ROA breakdown by sector |
| 🏭 Sector Comparison | Average revenue across all sectors |
| 🎛️ Interactive Filters | Filter by Year and Sector |
| ✨ UI Effects | Animated aurora background, glowing particle cursor trail |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| 🐍 Python | Core programming language |
| 📊 Plotly Dash | Interactive dashboard framework |
| 🐼 Pandas | Data manipulation and analysis |
| 🎨 CSS / HTML | Custom styling and animations |
| 🦄 Gunicorn | Production WSGI server |
| ☁️ Render | Cloud deployment platform |
| 🐙 GitHub | Version control |

---

## 📂 Dataset

- Source: Kaggle - Financial Statements of Major Companies 2009-2023
- Type: Real 10-K Annual Report Data
- Coverage: Fortune 500 companies across IT, Finance, Banking, Manufacturing and more
- Fields: Revenue, Net Income, EBITDA, Market Cap, ROE, ROA, Cash Flow, EPS and more

---

## 🧠 What I Learned

- How to build a fully interactive web application using Python and Plotly Dash
- How to load, clean and transform real-world financial datasets using Pandas
- How to implement callback functions to make dashboards dynamically interactive
- How to apply glassmorphism UI design principles using pure CSS
- How to deploy a Python web application to the cloud using Render and Gunicorn
- How to use Git and GitHub for version control in a real project workflow
- How to structure a production-grade project with proper file organisation

---

## 💪 Challenges and How I Solved Them

**Challenge 1 - Styling Dash dropdowns**
Dash dropdown components render inside React making CSS overrides very difficult. Solved by replacing dropdowns with custom pill-style filter buttons that are fully styleable and look more sophisticated.

**Challenge 2 - Deploying on Mac without Power BI Desktop**
Power BI Desktop is Windows-only. Solved by using Power BI Service in the browser for the first dashboard, then moved to Python/Plotly Dash for full control over design and deployment.

**Challenge 3 - Terminal filename conflicts**
VS Code terminal was auto-converting filenames to hyperlinks, breaking Python commands. Solved by using Mac native Terminal and the cat heredoc method to write files directly from command line.

**Challenge 4 - Git push rejections**
When adding README directly on GitHub while having local commits, Git rejected the push. Solved using git pull origin main --rebase before pushing.

---

## 🚀 How to Run Locally

Clone the repository
git clone https://github.com/jessicamathew31-coder/nexus-analytics.git

Navigate into the folder
cd nexus-analytics

Install dependencies
pip3 install -r requirements.txt

Run the dashboard
python3 run.py

Then open your browser and go to http://127.0.0.1:8050

---

## 👩 Built By

Jessica Mathew
MBA - Finance and Technology

LinkedIn: https://linkedin.com/in/jessicasmathew
Email: jessicamathew31@gmail.com

---

> Zero coding experience 3 weeks ago. Now I have a production-grade web application live on the internet.
'''

with open('README.md', 'w') as f:
    f.write(readme)
print("done")
