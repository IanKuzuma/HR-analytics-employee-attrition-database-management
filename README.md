---

# 👔 HR Analytics – Employee Attrition & Workforce Insights

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data--Analysis-yellow?logo=pandas)
![Seaborn](https://img.shields.io/badge/Seaborn-Visualization-teal?logo=plotly)
![Airflow](https://img.shields.io/badge/Airflow-Pipeline-blue?logo=apacheairflow)
![ElasticSearch](https://img.shields.io/badge/ElasticSearch-Kibana-green?logo=elasticsearch)
![GreatExpectations](https://img.shields.io/badge/GreatExpectations-Validation-orange?logo=checkmarx)

---

## 📌 Project Overview

This project takes a **descriptive analytics approach** to HR data, exploring **attrition drivers, performance ratings, promotions, and workforce patterns**. The goal is to provide **business-ready insights** through a validated and automated pipeline, ending with interactive dashboards for HR decision-makers.

Instead of just predicting churn, this project asks:

* Which job roles are most prone to attrition?
* Does overtime affect performance or retention?
* Are promotions and performance ratings aligned?
* Which departments face the most structural bottlenecks?

By validating and analyzing structured HR data, the project delivers **early warning signals** that companies can act on to improve retention and workforce planning.

🔗 **Links & References**

* [IBM HR Analytics Dataset](https://www.ibm.com/communities/analytics/watson-analytics-blog/hr-employee-attrition/) – Public dataset
* [Great Expectations Docs](https://docs.greatexpectations.io/) – Data quality framework

---

## 🏢 Problem Background

In any company, whether it’s a hot tech startup or a legacy manufacturer, **losing a good employee always stings**. You’re not just losing headcount—you’re losing experience, project momentum, team synergy, and spending a fortune to replace them.

Most companies still **react only after** someone resigns, rather than predicting *who* might be at risk and *why*.

This project aims to change that. By analyzing structured HR data, we uncover **patterns behind attrition and performance disparities**. The purpose isn’t just churn detection—it’s about giving HR a **data-driven way to support and retain talent proactively**.

---

## 🎯 Project Output

The final deliverable is a **complete data pipeline** that turns raw HR data into **validated insights and interactive dashboards**:

* ✅ **Exploratory Data Analysis (EDA):** attrition, performance, promotions, job roles
* ✅ **Visualizations:** pie chart, bar plots, line chart, heatmap, gauge chart
* ✅ **Interactive Dashboard:** deployed in **Kibana** on top of ElasticSearch
* ✅ **Data Validation:** automated checks via **Great Expectations**
* ✅ **Orchestration:** reproducible pipeline managed with **Apache Airflow**

The **core value** lies in surfacing **early indicators** of disengagement, mismatch, or organizational bottlenecks.

---

## 🧠 Method

This is a **descriptive analytics project** that combines **statistical exploration, visual storytelling, and data quality validation**.

### Steps Taken

* **Data Cleaning:** standardized columns, removed irrelevant fields (e.g. `EmployeeNumber`)
* **Feature Engineering:** tenure brackets, job level groupings, normalized ratings
* **Validation:** uniqueness checks, value ranges, categorical memberships with **Great Expectations**
* **Visualization Suite:**

  * 📊 **Pie Chart:** education distribution
  * 📊 **Bar Plots:** attrition by department & job role
  * 📈 **Line Chart:** avg. training time vs. years at company
  * 🔥 **Heatmap:** job levels across gender
  * 🎯 **Gauge Chart:** avg. years since last promotion

All outputs were integrated into **Kibana dashboards** for interactive exploration, with **Airflow DAGs** ensuring reproducibility.

---

## 📂 Repository Structure

```
📦 hr-analytics-attrition
 ┣ 📂 data                                                                        # Dataset storage
 ┣ 📂 dags                                                                        # Airflow pipeline DAGs
 ┣ 📂 gx                                                                          # Great Expectations config & Data Docs
 ┣ 📂 images                                                                      # Kibana plots screenshots
 ┣ 📜 HR_employee_attrition_dataset_raw.csv                                       # Dataset (Raw)
 ┣ 📜 HR_employee_attrition_dataset_clean.csv                                     # Dataset (processed)
 ┣ 📜 HR-analytics-employee-attrition-database-management-DAG.py                  # Airflow pipeline DAG python script
 ┣ 📜 HR-analytics-employee-attrition-database-management-GX.ipynb                # Jupyter notebooks for Great Expectations
 ┣ 📜 HR-analytics-employee-attrition-database-management-config.yaml             # yaml file to set up a data engineering stack
 ┣ 📜 HR-analytics-employee-attrition-database-management-ddl.txt                 # Postgesql query documentation
 ┣ 📜 HR-analytics-employee-attrition-database-management-table-query.sql         # Postgesql query file
 ┣ 📜 README.md                                                                   # Project documentation
```

---

## 🛠️ Tech Stack

* **Languages:** Python, YAML
* **Libraries:** pandas, seaborn, matplotlib, plotly, numpy
* **Validation:** Great Expectations
* **Orchestration:** Apache Airflow, Docker Compose
* **Database:** PostgreSQL
* **Visualization:** Kibana + ElasticSearch
* **Environment:** JupyterLab

---

## 📈 Results & Insights

* Dataset integrity confirmed: **1,470 rows, 35 features, no missing values**
* Interactive Kibana dashboard built with 6+ visualizations
* Clear signals detected in **attrition by job role, overtime, and promotion patterns**
* Validated pipeline ensures reproducibility and trust in insights

---

## 🙌 Acknowledgements

* Dataset: [IBM HR Analytics](https://www.ibm.com/communities/analytics/watson-analytics-blog/hr-employee-attrition/)
* Tools: Great Expectations, Apache Airflow, ElasticSearch/Kibana

---
