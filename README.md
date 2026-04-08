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

The expected score for team B is:

```text
E_B = 1 - E_A
```

### Rating update rule

After a match, ratings are updated using:

```text
R_new = R_old + K * (S - E)
```

where:
- `K` = update strength
- `S` = actual result (`1` for win, `0` for loss)
- `E` = expected result from Elo

### How predictions are generated

For an upcoming match:
1. the backend loads the regional Elo model
2. it looks up both teams’ current ratings
3. it computes win probabilities from the Elo gap
4. it assigns a confidence tier
5. it returns the predicted winner and probabilities to the frontend

### Why Elo is used right now

I use Elo as the current baseline because it is transparent and easy to validate. It gives a strong first version of the product while keeping the system understandable.

The long-term direction is to add more predictive features, such as:
- event context
- roster or team metadata
- recent form
- stage performance
- other structured features

Those can later be used in a stronger supervised model such as LightGBM, with Elo retained as one of the input features rather than the full model itself.

## Tech Stack

- **Programming Language:** Python  
  - Data processing: `pandas`, `numpy`
  - Web scraping / API access: `requests`, `cloudscraper`
  - Machine Learning / Statistics: Elo baseline now, with future plans for LightGBM
- **Backend Framework:** Flask
- **Frontend Framework:** React + TypeScript
- **Routing:** React Router
- **Data Source / API:** `vlrggapi`
- **Version Control:** Git + GitHub

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

### `GET /`
Healthcheck endpoint.

### `GET /upcoming-matches`
Returns upcoming VCT matches enriched with:
- predicted winner
- win probabilities
- Elo ratings
- confidence level
- team metadata (tag/logo when available)

### `GET /rankings/<region>`
Returns Elo rankings for a region such as:
- `pacific`
- `china`
- `emea`
- `americas`

Each ranking row includes:
- team
- team metadata
- rating
- matches played

## Getting Started

### Prerequisites

- **Python 3.x** installed on your system
- **Node.js & npm/yarn** for running the frontend
- **Git** for version control

### 1. Clone the repository

```bash
git clone https://github.com/Haxodrat/valesportsmodel.git
cd valesportsmodel
```

### 2. Backend Setup

Create and activate a Python virtual environment.

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install backend dependencies.

```bash
pip install -r requirements.txt
```

Create a `.env` file in `backend/` if needed:

```env
VLR_API_BASE_URL=http://localhost:3001
DEBUG=true
```

Run the backend:

```bash
python app.py
```

### 3. Frontend Setup

In a second terminal:

```bash
cd frontend
npm install
npm start
```

### 4. Local development flow

The app typically expects:
- React frontend on `localhost:3000`
- Flask backend on `localhost:5000`
- `vlrggapi` on `localhost:3001` or another configured base URL

## Data Sources

### `vlrggapi`
Used for:
- upcoming matches
- team profile metadata
- structured VLR-derived data

### `vlr.gg`
Used as the underlying match reference source and destination for user-facing links.

### Regional Elo snapshots
The project stores regional Elo model state as JSON in `backend/data/elo/`.

These snapshots include:
- current ratings
- matches played
- training match count
- model configuration
- final rankings

## Roadmap

- Add richer input features for prediction beyond Elo
- Use Elo as an input feature in a stronger model such as LightGBM
- Improve confidence calibration
- Expand automatic team metadata syncing
- Improve historical validation and evaluation
- Continue refining rankings and match presentation
- Extend tournament-oriented and bracket-oriented views over time

## Contact

- **Author:** Christopher Kim
- **LinkedIn:** https://www.linkedin.com/in/ckim259/
- **GitHub:** https://github.com/Haxodrat
- **Repository:** https://github.com/Haxodrat/valesportsmodel
- **Email:** haxodrat@icloud.com
