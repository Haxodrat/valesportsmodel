# TournVal

I wanted a way to easily see upcoming Valorant matches and see who'd most likely win.
A Valorant Esports Tournament Bracket Predictor that leverages historical data and statistical models to forecast match outcomes and generate tournament brackets. This project is designed for esports enthusiasts and developers interested in analytics and competitive gaming.

ValeSportsModel is a Valorant esports analytics web app for viewing upcoming VCT matches, Elo-based win probabilities, and regional team rankings across Pacific, China, EMEA, and Americas.

The project currently uses an Elo rating system as a lightweight, interpretable baseline for match prediction. The longer-term plan is to extend the feature set with richer data sources and use those features in a more advanced model such as LightGBM.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [How the Elo Rating Works](#how-the-elo-rating-works)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Getting Started](#getting-started)
- [Data Sources](#data-sources)
- [Roadmap](#roadmap)
- [Contact](#contact)

## Overview

**TournVal** is a side project aimed at providing predictions for Valorant esports tournaments. The project involves data collection, statistical analysis, and building an interactive frontend to display dynamic tournament brackets. Whether you're a fan looking to gauge likely outcomes or a developer keen on sports analytics, this project will give you insights into predictive modeling and API development.

ValeSportsModel was built to make Valorant esports predictions easier to browse and understand.

Instead of just listing upcoming matches, the app enriches each match with:
- a predicted winner
- win probabilities for both teams
- confidence labels based on the Elo spread
- regional Elo ratings
- ranking tables for each major VCT region

The frontend is a React + TypeScript dashboard, while the backend is a Flask API that loads regional Elo models, fetches upcoming matches from `vlrggapi`, and returns enriched prediction payloads for the UI.

## Features

- **Predictive Modeling:** Uses statistical algorithms (and potentially machine learning models) to predict match outcomes.
- **Bracket Visualization:** Dynamically generates and updates tournament brackets based on predictions.
- **Data Collection:** Integrates with popular esports data sources (or web-scraping methods) to gather historical and live match data.
- **API-Driven Architecture:** Provides RESTful endpoints for accessing predictions and tournament data.
- **Modular Design:** Clean separation between data collection, prediction engine, backend API, and frontend application.

### Upcoming match predictions
- Displays upcoming VCT matches
- Shows win probability for each team
- Shows predicted winner
- Shows Elo ratings for both teams
- Includes direct links to the match page on `vlr.gg`

### Regional Elo rankings
- Regional rankings for:
  - Pacific
  - China
  - EMEA
  - Americas
- Displays:
  - rank
  - team name
  - team tag
  - team logo
  - Elo rating
  - matches played

## How the Elo Rating Works

ValeSportsModel currently uses Elo as its primary rating system.

Elo is a simple rating method that updates team strength after each match based on:
- the current rating of both teams
- the expected outcome
- the actual outcome

### Core idea

Each team starts with a baseline rating. When two teams play:
- the stronger team is expected to win more often
- if the stronger team wins, ratings change only a little
- if the weaker team wins, ratings change more

This makes Elo useful for esports because it is:
- fast
- interpretable
- easy to update after every match
- a strong baseline before using more complex machine learning models

### Expected win probability

For two teams with ratings `R_A` and `R_B`, the expected score for team A is:

```text
E_A = 1 / (1 + 10^((R_B - R_A) / scale))
```


## Tech Stack

- **Programming Language:** Python  
  - Data processing: `pandas`, `numpy`
  - Web scraping: `requests`, `BeautifulSoup`, `Selenium` (if needed)
  - Machine Learning/Statistics: `scikit-learn`, potentially `TensorFlow` or `PyTorch`
- **Backend Framework:** Flask or FastAPI for building RESTful APIs
- **Frontend Framework:** React with visualization libraries like D3.js or Chart.js to render interactive brackets
- **Database:** PostgreSQL (or alternatives like MongoDB/SQLite for initial prototypes)
- **Version Control:** Git (hosted on GitHub, GitLab, or Bitbucket)
- **Deployment:** Docker for containerization; Heroku, AWS, or DigitalOcean for hosting

## Getting Started

### Prerequisites

- **Python 3.x** installed on your system
- **Node.js & npm/yarn** for running the frontend (if building a web interface)
- **Git** for version control

### Setup Instructions

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/valesportsmodel.git
   cd valesportsmodel

2. **Backend Setup:**

   Create and activate a Python virtual environment.
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

   Install backend dependencies.
   ```bash
   pip install -r requirements.txt
   ```

   Create a .env file for configuration (e.g., API keys, database connection settings).

   Run the Flask/FastAPI application:
   ```bash
   python3 app.py
   ```
3. **Frontend Setup:**

   Create a react template using TypeScript.
   ```bash
   npx create-react-app frontend --template typescript
   ```

   Install frontend dependencies from package.json.
   ```bash
   cd frontend
   npm install
   ```

   Run the server:
   ```bash
   npm start
   ```

## Project Structure
```bash
valesportsmodel/
├── backend/
│   ├── app.py                    # Flask app entrypoint
│   ├── api.py                    # Blueprint registration
│   ├── configs/
│   │   └── config.py             # Environment-backed configuration
│   ├── data/
│   │   └── team_ids.json         # Team name -> VLR team ID mapping
│   ├── data_sources/
│   │   └── vlr_client.py         # VLRGG API client
│   ├── routes/
│   │   ├── matches.py            # Upcoming match endpoints
│   │   └── rankings.py           # Regional rankings endpoints
│   ├── services/
│   │   ├── predictions.py        # Match prediction enrichment
│   │   ├── rankings.py           # Rankings loading / filtering
│   │   └── team_metadata.py      # Team tag/logo enrichment
│   ├── ratings/
│   │   └── elo.py                # Elo model implementation
│   └── data/elo/                 # Saved Elo model JSON snapshots
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── api/                  # Frontend API helpers
│   │   ├── components/           # UI components
│   │   ├── hooks/                # Data fetching hooks
│   │   ├── pages/                # Route-level pages
│   │   ├── types/                # Shared frontend types
│   │   ├── utils/                # Frontend formatting helpers
│   │   ├── App.tsx
│   │   ├── App.css
│   │   └── index.tsx
│   └── package.json
│
└── README.md
```

## API Endpoints

GET / - healthcheck endpoint

GET /upcoming-matches - returns upcoming VCT matches enriched with:


## Contact
#### Linkedin: https://www.linkedin.com/in/ckim259/
