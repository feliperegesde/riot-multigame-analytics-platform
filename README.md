# 🎮 Riot Games Multi-Game Analytics Platform

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Machine%20Learning-KMeans-orange.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

A robust, modular data analytics and scouting web application designed to track, process, and evaluate deep performance metrics across competitive multiplayer titles (**League of Legends** and **Valorant**). Moving far beyond standard public trackers, this platform parses raw JSON payloads from official and community APIs, extracts advanced in-game indicators (such as Damage Share, Gold Generation, Vision Control, and Combat Scores), and applies Unsupervised Machine Learning (**K-Means Clustering**) to categorize player behaviors and playstyles.

---

## 🚀 Key Features

* **Multi-Game Architecture:** Cleanly decoupled domain structure supporting independent data ingestion pipelines for *League of Legends* (Riot Games Official API) and *Valorant* (HenrikDev Public API).
* **Advanced Metrics Processing:** 
  * **LoL:** Calculates Damage Share Percentage relative to the team, Gold Earned evolution, Vision Score efficiency, and CS per minute.
  * **Valorant:** Analyzes Average Combat Score (ACS), KDA distributions, agent pool history, and round impact.
* **Playstyle Clustering (Machine Learning):** Implements `scikit-learn`'s `KMeans` and `StandardScaler` to normalize performance features and automatically classify matches into distinct behavior clusters (e.g., *Strategic / Objective-Focused* vs. *Aggressive / Combat-Oriented*).
* **Interactive Dashboard:** Built with **Streamlit**, featuring multi-tab deep dives, dynamic KPIs, and interactive visual charts for performance evolution.
* **Production-Ready Code Quality:** Organized into modular domain folders following clean software design principles, completely free of redundant execution blocks.

---

## 📂 Project Architecture

```text
riot-multigame-platform/
│
├── src/
│   ├── lol/
│   │   ├── __init__.py
│   │   ├── api_client.py       # Riot Games API integration (Account-V1 & Match-V5)
│   │   └── processor.py        # Data cleaning, damage share, and metric extraction
│   ├── valorant/
│   │   ├── __init__.py
│   │   ├── api_client.py       # HenrikDev Valorant API integration
│   │   └── processor.py        # ACS, map stats, and combat score parsing
│   └── shared/
│       ├── __init__.py
│       └── cluster_model.py    # Reusable unsupervised ML pipeline (K-Means)
│
├── app.py                      # Central Streamlit multi-page dashboard interface
└── requirements.txt            # Project dependencies