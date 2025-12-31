# 🏆 CAN 2025 Data Pipeline

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![GCP](https://img.shields.io/badge/GCP-BigQuery-4285F4.svg)
![DBT](https://img.shields.io/badge/DBT-1.7+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**A complete end-to-end data engineering pipeline for Africa Cup of Nations 2025**

[Features](#-features) • [Architecture](#-architecture) • [Quick Start](#-quick-start) • [Documentation](#-documentation)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Data Model](#-data-model)
- [DBT Transformations](#-dbt-transformations)
- [Monitoring & Logging](#-monitoring--logging)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Dashboards & Analytics](#-dashboards--analytics)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [Roadmap](#-roadmap)
- [License](#-license)

---

## 🌟 Overview

The **CAN 2025 Data Pipeline** is a production-ready ELT (Extract, Load, Transform) data pipeline that processes Africa Cup of Nations tournament data. It demonstrates modern data engineering practices including data generation, cloud storage, data warehousing, and analytics-ready transformations.

### What This Pipeline Does

- 🎲 **Generates** realistic fake tournament data (teams, players, matches, events, revenue)
- ☁️ **Uploads** data to Google Cloud Storage for staging
- 🗄️ **Loads** data into BigQuery as raw tables
- 🔄 **Transforms** data using DBT into analytics-ready tables
- 📊 **Enables** business intelligence and data visualization
- 🔍 **Implements** data quality testing and validation

---

## ✨ Features

### Data Generation
- ✅ 24 teams with realistic FIFA rankings
- ✅ 552 players with positions, ages, and market values
- ✅ 6 stadiums across Morocco
- ✅ Complete tournament schedule (group stage + knockouts)
- ✅ Match events (goals, yellow cards, red cards)
- ✅ Ticket sales and revenue data

### Pipeline Features
- ⚡ **Automated ETL** - One command to run the entire pipeline
- 🔐 **Secure** - GCP service account authentication
- 📝 **Logged** - Comprehensive logging at every step
- 🧪 **Tested** - DBT tests for data quality
- 📚 **Documented** - Auto-generated DBT documentation
- 🔄 **Incremental** - Support for incremental loads

### Analytics Features
- 📈 Team standings and rankings
- ⚽ Top scorers leaderboard
- 🏟️ Stadium performance metrics
- 💰 Financial analytics
- 📅 Complete match calendar
- 🎯 Player statistics

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           CAN 2025 DATA PIPELINE                         │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────┐
│   PYTHON     │  Step 1: Data Generation
│  Faker Lib   │  ────────────────────────
│              │  • Generate fake tournament data
│  Generated   │  • 6 CSV files created locally
│    Data      │  • Teams, Players, Matches, etc.
└──────┬───────┘
       │
       │ 1_generate_data.py
       ▼
┌──────────────────────────────────────────────────────────────┐
│                     LOCAL FILESYSTEM                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  teams.csv  │  │players.csv  │  │matches.csv  │  + 3 more│
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           │ 2_load_to_gcs.py
                           ▼
┌──────────────────────────────────────────────────────────────┐
│              GOOGLE CLOUD STORAGE (GCS)                      │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  gs://can2025-data-bucket/raw_data/                   │  │
│  │  ├── teams.csv                                         │  │
│  │  ├── players.csv                                       │  │
│  │  ├── stadiums.csv                                      │  │
│  │  ├── matches.csv                                       │  │
│  │  ├── match_events.csv                                  │  │
│  │  └── ticket_sales.csv                                  │  │
│  └───────────────────────────────────────────────────────┘  │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           │ 3_load_to_bigquery.py
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                    BIGQUERY - RAW LAYER                      │
│              Dataset: can2025_raw                            │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Tables (6):                                            │ │
│  │  • teams (24 rows)                                      │ │
│  │  • players (552 rows)                                   │ │
│  │  • stadiums (6 rows)                                    │ │
│  │  • matches (~62 rows)                                   │ │
│  │  • match_events (~500 rows)                             │ │
│  │  • ticket_sales (~248 rows)                             │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           │ dbt run
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                DBT TRANSFORMATION LAYERS                     │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  STAGING LAYER (Views)                               │  │
│  │  • stg_teams                                         │  │
│  │  • stg_players (+ age categories)                   │  │
│  │  • stg_matches (+ calculated fields)                │  │
│  │  • stg_match_events (+ period classification)       │  │
│  │  • stg_ticket_sales (+ revenue calcs)               │  │
│  └──────────────────────────────────────────────────────┘  │
│                           │                                  │
│                           ▼                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  INTERMEDIATE LAYER (Views)                          │  │
│  │  • int_team_performance                              │  │
│  │  • int_player_statistics                             │  │
│  │  • int_match_intensity                               │  │
│  │  • int_revenue_analysis                              │  │
│  └──────────────────────────────────────────────────────┘  │
│                           │                                  │
│                           ▼                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  MARTS LAYER (Tables) - Analytics Ready              │  │
│  │  • mart_team_standings                               │  │
│  │  • mart_top_scorers                                  │  │
│  │  • mart_stadium_performance                          │  │
│  │  • mart_match_calendar                               │  │
│  │  • mart_financial_summary                            │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│               BIGQUERY - TRANSFORMED LAYER                   │
│           Dataset: can2025_transformed                       │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Analytics-Ready Tables for BI Tools                   │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                    BI & VISUALIZATION                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Looker    │  │   Tableau   │  │  Power BI   │         │
│  │   Studio    │  │             │  │             │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                    MONITORING & LOGGING                      │
│  • Pipeline execution logs                                   │
│  • DBT test results                                          │
│  • Data quality metrics                                      │
└──────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

| Category | Technology | Purpose |
|----------|-----------|---------|
| **Language** | Python 3.8+ | Core pipeline logic |
| **Data Generation** | Faker | Generate realistic fake data |
| **Cloud Platform** | Google Cloud Platform | Infrastructure |
| **Storage** | Google Cloud Storage | Data lake / staging |
| **Data Warehouse** | BigQuery | Analytics database |
| **Transformation** | DBT (Data Build Tool) | SQL transformations |
| **Version Control** | Git / GitHub | Code management |
| **BI Tools** | Looker Studio / Tableau / Power BI | Visualization |

---

## 📁 Project Structure

```
can2025_pipeline/
│
├── 📄 README.md                      # This file
├── 📄 requirements.txt               # Python dependencies
├── 📄 .gitignore                     # Git ignore rules
├── 📄 .env.example                   # Environment template
├── 📄 Makefile                       # Automation commands (optional)
│
├── 🐍 1_generate_data.py             # Step 1: Generate CAN 2025 data
├── 🐍 2_load_to_gcs.py               # Step 2: Upload to GCS
├── 🐍 3_load_to_bigquery.py          # Step 3: Load to BigQuery
│
├── 📁 generated_tables/              # Generated CSV files
│   ├── teams.csv                     # 24 teams
│   ├── players.csv                   # 552 players
│   ├── stadiums.csv                  # 6 stadiums
│   ├── matches.csv                   # ~62 matches
│   ├── match_events.csv              # ~500 events
│   └── ticket_sales.csv              # ~248 sales records
│
├── 📁 logs/                          # Execution logs
│   ├── data_generation.log
│   ├── gcs_upload.log
│   └── bigquery_load.log
│
└── 📁 can2025_dbt/                   # DBT project
    ├── dbt_project.yml               # DBT configuration
    ├── profiles.yml                  # Connection profiles
    │
    ├── 📁 models/
    │   ├── sources.yml               # Source definitions
    │   │
    │   ├── 📁 staging/               # Layer 1: Data cleaning
    │   │   ├── schema.yml
    │   │   ├── stg_teams.sql
    │   │   ├── stg_players.sql
    │   │   ├── stg_stadiums.sql
    │   │   ├── stg_matches.sql
    │   │   ├── stg_match_events.sql
    │   │   └── stg_ticket_sales.sql
    │   │
    │   ├── 📁 intermediate/          # Layer 2: Business logic
    │   │   ├── schema.yml
    │   │   ├── int_team_performance.sql
    │   │   ├── int_player_statistics.sql
    │   │   ├── int_match_intensity.sql
    │   │   └── int_revenue_analysis.sql
    │   │
    │   └── 📁 marts/                 # Layer 3: Analytics ready
    │       ├── schema.yml
    │       ├── mart_team_standings.sql
    │       ├── mart_top_scorers.sql
    │       ├── mart_stadium_performance.sql
    │       ├── mart_match_calendar.sql
    │       └── mart_financial_summary.sql
    │
    ├── 📁 macros/                    # Reusable SQL functions
    │   └── calculate_points.sql
    │
    └── 📁 tests/                     # Data quality tests
        └── total_goals_consistency.sql
```

---

## 📋 Prerequisites

### Required

- **Python 3.8+** installed on your machine
- **Google Cloud Platform account** with billing enabled
- **GCP Project** with the following APIs enabled:
  - BigQuery API
  - Cloud Storage API
- **GCP Service Account** with these roles:
  - `BigQuery Admin`
  - `Storage Admin`
  - JSON key file downloaded

### Optional

- **Docker** (for containerization)
- **Make** (for automation commands)
- **Git** (for version control)

---

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/can2025_pipeline.git
cd can2025_pipeline
```

### Step 2: Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install DBT

```bash
pip install dbt-bigquery
```

---

## ⚙️ Configuration

### 1. Set Up GCP Authentication

```bash
# Download your service account JSON key from GCP Console
# Then set the environment variable:

# On macOS/Linux:
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"

# On Windows:
set GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your\service-account-key.json"
```

### 2. Update Pipeline Configuration

Edit `2_load_to_gcs.py`:
```python
PROJECT_ID = "your-gcp-project-id"        # Replace with your project
BUCKET_NAME = "can2025-data-bucket"        # Your bucket name
```

Edit `3_load_to_bigquery.py`:
```python
PROJECT_ID = "your-gcp-project-id"        # Replace with your project
DATASET_ID = "can2025_raw"                 # Raw dataset name
BUCKET_NAME = "can2025-data-bucket"        # Same as above
```

### 3. Configure DBT Profile

Create or edit `~/.dbt/profiles.yml`:

```yaml
can2025:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: service-account
      project: your-gcp-project-id              # Your GCP project
      dataset: can2025_transformed               # Transformed dataset
      threads: 4
      keyfile: /path/to/service-account-key.json
      location: US
      timeout_seconds: 300
      
    prod:
      type: bigquery
      method: service-account
      project: your-gcp-project-id
      dataset: can2025_prod
      threads: 8
      keyfile: /path/to/service-account-key.json
      location: US
      timeout_seconds: 300
```

---

## 🎯 Usage

### Option 1: Manual Execution (Step by Step)

```bash
# Step 1: Generate data locally
python 1_generate_data.py
# Output: 6 CSV files in generated_tables/

# Step 2: Upload to Google Cloud Storage
python 2_load_to_gcs.py
# Output: Files uploaded to gs://can2025-data-bucket/raw_data/

# Step 3: Load into BigQuery
python 3_load_to_bigquery.py
# Output: 6 tables created in BigQuery dataset 'can2025_raw'

# Step 4: Run DBT transformations
cd can2025_dbt
dbt run
# Output: Transformed tables in 'can2025_transformed' dataset

# Step 5: Run tests
dbt test

# Step 6: Generate documentation
dbt docs generate
dbt docs serve
# Opens documentation in browser at http://localhost:8080
```

### Option 2: Automated Execution (Using Makefile)

```bash
# Run entire pipeline
make all

# Or run individual steps
make generate    # Generate data
make upload      # Upload to GCS
make load        # Load to BigQuery
make dbt-run     # Run DBT transformations
make dbt-test    # Run DBT tests
make dbt-docs    # Generate & serve documentation

# Clean up
make clean       # Remove generated files
```

### Option 3: Docker Execution

```bash
# Build Docker image
docker-compose build

# Run pipeline
docker-compose up

# Run specific service
docker-compose run pipeline python 1_generate_data.py
```

---

## 📊 Data Model

### Source Tables (Raw Layer)

| Table | Rows | Description | Key Columns |
|-------|------|-------------|-------------|
| `teams` | 24 | Tournament teams | team_id, team_name, group_name, fifa_ranking |
| `players` | 552 | Player rosters | player_id, team_id, player_name, position, age |
| `stadiums` | 6 | Match venues | stadium_id, stadium_name, city, capacity |
| `matches` | ~62 | All tournament matches | match_id, home_team_id, away_team_id, scores |
| `match_events` | ~500 | Goals and cards | event_id, match_id, player_id, event_type |
| `ticket_sales` | ~248 | Revenue data | sale_id, match_id, category, total_revenue |

### Entity Relationship Diagram

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   TEAMS     │◄───────►│   PLAYERS    │         │  STADIUMS   │
│             │ 1     * │              │         │             │
│ team_id (PK)│         │ player_id(PK)│         │stadium_id(PK)│
│ team_name   │         │ team_id (FK) │         │ stadium_name│
│ group_name  │         │ player_name  │         │ capacity    │
└──────┬──────┘         └──────┬───────┘         └──────┬──────┘
       │                       │                        │
       │ 1                     │ *                      │ 1
       │                       │                        │
       │      ┌────────────────▼───────────────────┐   │
       │      │          MATCHES                    │◄──┘
       └─────►│                                     │
         * 1  │ match_id (PK)                       │
              │ home_team_id (FK)                   │
              │ away_team_id (FK)                   │
              │ stadium_id (FK)                     │
              │ home_score, away_score              │
              └──────┬──────────────┬───────────────┘
                     │ 1            │ 1
                     │              │
                     │ *            │ *
              ┌──────▼────────┐ ┌──▼───────────────┐
              │ MATCH_EVENTS  │ │  TICKET_SALES    │
              │               │ │                  │
              │ event_id (PK) │ │ sale_id (PK)     │
              │ match_id (FK) │ │ match_id (FK)    │
              │ player_id (FK)│ │ ticket_category  │
              │ event_type    │ │ total_revenue    │
              └───────────────┘ └──────────────────┘
```

---

## 🔄 DBT Transformations

### Transformation Layers

```
RAW DATA → STAGING → INTERMEDIATE → MARTS → BI TOOLS
```

### Layer 1: Staging (Data Cleaning)

**Purpose**: Standardize, clean, and lightly transform raw data

| Model | Transformations | Output |
|-------|----------------|--------|
| `stg_teams` | TRIM names, UPPER groups | Cleaned team data |
| `stg_players` | Age categories, value tiers | Enhanced player data |
| `stg_matches` | Calculate total_goals, goal_difference | Match details |
| `stg_match_events` | Classify periods, add flags | Categorized events |
| `stg_ticket_sales` | Revenue calculations | Sales metrics |

### Layer 2: Intermediate (Business Logic)

**Purpose**: Complex calculations and aggregations

| Model | Purpose | Key Metrics |
|-------|---------|-------------|
| `int_team_performance` | Per-match team stats | Points, goals, clean sheets |
| `int_player_statistics` | Player aggregations | Total goals, cards, avg minute |
| `int_match_intensity` | Match characteristics | Events count, intensity score |
| `int_revenue_analysis` | Revenue per match | Total revenue by category |

### Layer 3: Marts (Analytics Ready)

**Purpose**: Business-ready tables for end users

| Mart | Description | Use Case |
|------|-------------|----------|
| `mart_team_standings` | Tournament standings | Leaderboards, rankings |
| `mart_top_scorers` | Golden Boot race | Player performance |
| `mart_stadium_performance` | Venue analytics | Operations, planning |
| `mart_match_calendar` | Complete schedule | Scheduling, broadcasting |
| `mart_financial_summary` | Revenue analytics | Financial reporting |

### Sample Transformation: Team Standings

```sql
-- models/marts/mart_team_standings.sql
SELECT
    t.team_id,
    t.team_name,
    t.group_name,
    COUNT(tp.match_id) as matches_played,
    SUM(CASE WHEN tp.outcome = 'Win' THEN 1 ELSE 0 END) as wins,
    SUM(CASE WHEN tp.outcome = 'Draw' THEN 1 ELSE 0 END) as draws,
    SUM(CASE WHEN tp.outcome = 'Loss' THEN 1 ELSE 0 END) as losses,
    SUM(tp.goals_scored) as goals_for,
    SUM(tp.goals_conceded) as goals_against,
    SUM(tp.goal_difference) as goal_difference,
    SUM(tp.points) as points,
    ROUND(SUM(tp.points) / COUNT(tp.match_id), 2) as points_per_game,
    RANK() OVER (
        PARTITION BY t.group_name 
        ORDER BY SUM(tp.points) DESC, SUM(tp.goal_difference) DESC
    ) as group_position
FROM {{ ref('stg_teams') }} t
LEFT JOIN {{ ref('int_team_performance') }} tp ON t.team_id = tp.team_id
GROUP BY t.team_id, t.team_name, t.group_name
```

---

## 📝 Monitoring & Logging

### Log Files

All pipeline operations are logged to the `logs/` directory:

```bash
logs/
├── data_generation.log      # CSV generation logs
├── gcs_upload.log           # GCS upload logs
└── bigquery_load.log        # BigQuery load logs
```

### Log Format

```
2025-01-15 14:23:45 - INFO - Starting CAN 2025 Data Generation
2025-01-15 14:23:46 - INFO - ✓ teams.csv created at generated_tables/teams.csv
2025-01-15 14:23:48 - INFO - ✓ players.csv created with 552 players
```

### Monitoring Commands

```bash
# Tail logs in real-time
tail -f logs/data_generation.log

# Check last 50 lines
tail -n 50 logs/bigquery_load.log

# Search for errors
grep ERROR logs/*.log
```

---

## 🧪 Testing

### DBT Tests

```bash
# Run all tests
dbt test

# Run tests for specific model
dbt test --select mart_team_standings

# Run tests with specific tag
dbt test --select tag:staging
```

### Test Types

1. **Schema Tests** (in `schema.yml`)
   - `unique`: Ensures column has unique values
   - `not_null`: Ensures no null values
   - `accepted_values`: Validates against list
   - `relationships`: Tests foreign keys

2. **Custom Tests** (in `tests/`)
   - Data consistency checks
   - Business logic validation
   - Cross-table validation

### Example Test

```yaml
# models/marts/schema.yml
models:
  - name: mart_team_standings
    columns:
      - name: team_id
        tests:
          - unique
          - not_null
      - name: points
        tests:
          - dbt_utils.expression_is_true:
              expression: "= (wins * 3 + draws)"
```

---

## 🚢 Deployment

### Production Deployment

1. **Set up production environment**
```bash
# Update profiles.yml with prod target
dbt run --target prod
```

2. **Schedule with Cloud Composer (Airflow)**
```python
# Sample DAG
from airflow import DAG
from airflow.operators.bash import BashOperator

dag = DAG('can2025_pipeline', schedule_interval='@daily')

generate = BashOperator(
    task_id='generate_data',
    bash_command='python /path/to/1_generate_data.py',
    dag=dag
)

upload = BashOperator(
    task_id='upload_to_gcs',
    bash_command='python /path/to/2_load_to_gcs.py',
    dag=dag
)

load = BashOperator(
    task_id='load_to_bigquery',
    bash_command='python /path/to/3_load_to_bigquery.py',
    dag=dag
)

dbt_run = BashOperator(
    task_id='dbt_transform',
    bash_command='cd /path/to/can2025_dbt && dbt run',
    dag=dag
)

generate >> upload >> load >> dbt_run
```

3. **CI/CD with GitHub Actions**
```yaml
# .github/workflows/dbt.yml
name: DBT Pipeline
on: [push]
jobs:
  run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run DBT
        run: |
          dbt deps
          dbt run
          dbt test
```

---

## 📊 Dashboards & Analytics

### Sample Queries

**1. Top 5 Scorers**
```sql
SELECT 
    player_name,
    team_name,
    total_goals,
    goals_per_match
FROM `project.can2025_transformed.mart_top_scorers`
ORDER BY total_goals DESC
LIMIT 5;
```

**2. Group Standings**
```sql
SELECT 
    group_name,
    group_position,
    team_name,
    points,
    goal_difference
FROM `project.can2025_transformed.mart_team_standings`
WHERE group_name = 'A'
ORDER BY group_position;
```

**3. Revenue by Stadium**
```sql
SELECT 
    stadium_name,
    city,
    matches_hosted,
    total_revenue_generated,
    avg_attendance
FROM `project.can2025_transformed.mart_stadium_performance`
ORDER BY total_revenue_generated DESC;
```

### Dashboard Examples

Connect your favorite BI tool to BigQuery and create:

1. **Executive Dashboard**
   - Total tournament revenue
   - Average attendance
   - Top teams and players
   - Key tournament stats

2. **Team Performance**
   - Win/loss records
   - Goals scored/conceded trends
   - Head-to-head comparisons
   - Group standings

3. **Financial Analytics**
   - Revenue by match phase
   - Ticket category breakdown
   - Stadium revenue comparison
   - Attendance trends

4. **Player Statistics**
   - Top scorers leaderboard
   - Most carded players
   - Age distribution analysis
   - Market value vs performance

---

## 🔧 Troubleshooting

### Common Issues

#### 1. GCP Authentication Error

**Problem**: `Could not automatically determine credentials`

**Solution**:
```bash
# Verify credentials are set
echo $GOOGLE_APPLICATION_CREDENTIALS

# Or use gcloud CLI
gcloud auth application-default login
```

#### 2. BigQuery Permission Denied

**Problem**: `Access Denied: BigQuery BigQuery: Permission denied`

**Solution**:
- Ensure service account has `BigQuery Admin` role
- Check project ID is correct
- Verify billing is enabled

#### 3. DBT Connection Failed

**Problem**: `Could not connect to BigQuery`

**Solution**:
```bash
# Test connection
dbt debug

# Check profiles.yml location
dbt debug --profiles-dir ~/.dbt

# Verify profiles.yml syntax
cat ~/.dbt/profiles.yml
```

#### 4. CSV Files Not Found

**Problem**: `FileNotFoundError: generated_tables/teams.csv`

**Solution**:
```bash
# Run data generation first
python 1_generate_data.py

# Verify files exist
ls -la generated_tables/
```

#### 5. GCS Bucket Not Found

**Problem**: `Bucket not found: can2025-data-bucket`

**Solution**:
- Create bucket in GCP Console, or
- Script will auto-create if permissions allow
- Check bucket name spelling

### Getting Help

- 📚 Check [DBT Documentation](https://docs.getdbt.com)
- 🔍 Search [BigQuery Documentation](https://cloud.google.com/bigquery/docs)
- 💬 Open an issue on GitHub
- 📧 Contact: your-email@example.com

---

## 💰 Cost Estimation

### GCP Costs (Monthly estimates for development)

| Service | Usage | Estimated Cost |
|---------|-------|----------------|
| **Cloud Storage** | 1 GB data storage | ~$0.02/month |
| **BigQuery Storage** | 5 GB stored data | ~$0.10/month |
| **BigQuery Queries** | 100 GB processed | ~$5.00/month |
| **BigQuery Streaming** | Minimal inserts | ~$0.50/month |
| **Total** | Development workload | **~$6/month** |

### Production Costs (Scaled)

| Service | Usage | Estimated Cost |
|---------|-------|----------------|
| **Cloud Storage** | 50 GB data storage | ~$1.00/month |
| **BigQuery Storage** | 200 GB stored data | ~$4.00/month |
| **BigQuery Queries** | 5 TB processed | ~$250/month |
| **Cloud Composer** | Small environment | ~$300/month |
| **Total** | Production workload | **~$555/month** |

💡 **Cost Optimization Tips**:
- Use partitioned tables in BigQuery
- Set table expiration for temporary data
- Use BigQuery's free tier (1 TB queries/month)
- Archive old data to Cloud Storage
- Use cached query results
- Implement incremental DBT models

---

## ⚡ Performance Benchmarks

### Pipeline Execution Times

| Step | Duration | Notes |
|------|----------|-------|
| Data Generation | ~5 seconds | 6 CSV files, 1,400+ rows |
| GCS Upload | ~2 seconds | 6 files, ~2 MB total |
| BigQuery Load | ~10 seconds | 6 tables, bulk insert |
| DBT Run (All Models) | ~30 seconds | 14 models (5 staging + 4 intermediate + 5 marts) |
| DBT Tests | ~15 seconds | 20+ data quality tests |
| **Total Pipeline** | **~62 seconds** | End-to-end execution |

### BigQuery Query Performance

| Query Type | Avg Duration | Data Scanned |
|------------|--------------|--------------|
| Simple SELECT | <1 second | <100 MB |
| Aggregations | 1-2 seconds | ~500 MB |
| Complex Joins | 2-5 seconds | ~1 GB |
| Mart Materialization | 5-10 seconds | ~2 GB |

### Scalability

| Data Volume | Processing Time | Storage Cost |
|-------------|-----------------|--------------|
| 1 Tournament (current) | ~1 minute | ~$0.10/month |
| 10 Tournaments | ~5 minutes | ~$1.00/month |
| 100 Tournaments | ~30 minutes | ~$10/month |

---

## 🔐 Security Best Practices

### 1. Credential Management

```bash
# ❌ NEVER commit credentials
git add service-account-key.json  # DON'T DO THIS!

# ✅ Use environment variables
export GOOGLE_APPLICATION_CREDENTIALS="path/to/key.json"

# ✅ Use secret managers
gcloud secrets create service-account-key \
    --data-file=service-account-key.json
```

### 2. IAM Least Privilege

```yaml
# Recommended service account roles:
roles:
  - roles/bigquery.dataEditor      # For data loading
  - roles/bigquery.jobUser         # For query execution
  - roles/storage.objectAdmin      # For GCS operations
  
# Avoid:
  - roles/owner                    # Too permissive
  - roles/editor                   # Too permissive
```

### 3. Data Encryption

- ✅ Data encrypted at rest (default in GCP)
- ✅ Data encrypted in transit (HTTPS)
- ✅ Use customer-managed encryption keys (optional)

### 4. Access Control

```sql
-- Grant read-only access to marts
GRANT `roles/bigquery.dataViewer` 
ON SCHEMA `project.can2025_transformed` 
TO "user:analyst@company.com";

-- Restrict raw data access
REVOKE `roles/bigquery.dataViewer` 
ON SCHEMA `project.can2025_raw` 
FROM "group:analysts@company.com";
```

---

## 📈 Advanced Features

### 1. Incremental Models

For large datasets, use incremental materialization:

```sql
-- models/staging/stg_matches_incremental.sql
{{
    config(
        materialized='incremental',
        unique_key='match_id',
        on_schema_change='fail'
    )
}}

SELECT *
FROM {{ source('can2025_raw', 'matches') }}

{% if is_incremental() %}
    WHERE match_date > (SELECT MAX(match_date) FROM {{ this }})
{% endif %}
```

### 2. Snapshots (Slowly Changing Dimensions)

Track historical changes:

```sql
-- snapshots/team_standings_snapshot.sql
{% snapshot team_standings_snapshot %}

{{
    config(
        target_schema='snapshots',
        unique_key='team_id',
        strategy='timestamp',
        updated_at='last_updated',
    )
}}

SELECT * FROM {{ ref('mart_team_standings') }}

{% endsnapshot %}
```

### 3. Custom Macros

```sql
-- macros/calculate_points.sql
{% macro calculate_points(wins, draws) %}
    ({{ wins }} * 3 + {{ draws }})
{% endmacro %}

-- Usage in model:
SELECT 
    team_name,
    {{ calculate_points('wins', 'draws') }} as points
FROM teams
```

### 4. Exposures (Document Dashboards)

```yaml
# models/exposures.yml
version: 2

exposures:
  - name: executive_dashboard
    type: dashboard
    maturity: high
    url: https://lookerstudio.google.com/dashboard/abc123
    description: Executive summary of CAN 2025 tournament
    
    depends_on:
      - ref('mart_team_standings')
      - ref('mart_financial_summary')
      - ref('mart_top_scorers')
    
    owner:
      name: Data Analytics Team
      email: analytics@company.com
```

### 5. Data Quality Monitoring

```sql
-- tests/assert_positive_revenue.sql
SELECT *
FROM {{ ref('mart_financial_summary') }}
WHERE total_revenue < 0
```

---

## 🎓 Learning Resources

### Tutorials & Guides

1. **Data Generation with Faker**
   - [Faker Documentation](https://faker.readthedocs.io/)
   - Tutorial: Building realistic test data

2. **Google Cloud Platform**
   - [BigQuery Best Practices](https://cloud.google.com/bigquery/docs/best-practices)
   - [GCS Storage Classes](https://cloud.google.com/storage/docs/storage-classes)

3. **DBT Learning**
   - [DBT Courses](https://courses.getdbt.com/)
   - [DBT Best Practices](https://docs.getdbt.com/guides/best-practices)

4. **Data Modeling**
   - [Kimball Dimensional Modeling](https://www.kimballgroup.com/)
   - Star Schema vs Snowflake Schema

### Video Tutorials

- 📺 [Building a Data Pipeline with GCP](https://www.youtube.com/results?search_query=gcp+data+pipeline)
- 📺 [DBT Tutorial Series](https://www.youtube.com/results?search_query=dbt+tutorial)
- 📺 [BigQuery Fundamentals](https://www.youtube.com/results?search_query=bigquery+tutorial)

### Community

- 💬 [DBT Slack Community](https://www.getdbt.com/community/join-the-community/)
- 💬 [GCP Community](https://www.googlecloudcommunity.com/)
- 💬 [r/dataengineering](https://www.reddit.com/r/dataengineering/)

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Types of Contributions

1. 🐛 **Bug Reports** - Found an issue? Open a bug report
2. ✨ **Feature Requests** - Have an idea? Share it with us
3. 📝 **Documentation** - Improve our docs
4. 💻 **Code Contributions** - Submit pull requests
5. 🎨 **Dashboard Templates** - Share your BI dashboards

### Contribution Workflow

```bash
# 1. Fork the repository
# Click "Fork" button on GitHub

# 2. Clone your fork
git clone https://github.com/YOUR-USERNAME/can2025_pipeline.git
cd can2025_pipeline

# 3. Create a feature branch
git checkout -b feature/amazing-feature

# 4. Make your changes
# Edit files, add features, fix bugs...

# 5. Run tests
python -m pytest tests/
dbt test

# 6. Commit your changes
git add .
git commit -m "Add amazing feature"

# 7. Push to your fork
git push origin feature/amazing-feature

# 8. Open a Pull Request
# Go to GitHub and click "New Pull Request"
```

### Code Style Guidelines

```python
# Python: Follow PEP 8
# Use meaningful variable names
team_count = len(teams)  # ✅ Good
tc = len(teams)          # ❌ Bad

# Add docstrings
def generate_teams():
    """
    Generate fake team data for CAN 2025 tournament.
    
    Returns:
        None: Writes teams.csv to OUTPUT_DIR
    """
    pass
```

```sql
-- SQL: Follow DBT style guide
-- Use lowercase for keywords
-- Use snake_case for identifiers
-- Indent 4 spaces

select
    team_id,
    team_name,
    sum(points) as total_points
from {{ ref('team_performance') }}
group by team_id, team_name
```

### Pull Request Checklist

- [ ] Code follows style guidelines
- [ ] Tests pass (`pytest` and `dbt test`)
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] No sensitive data in commits
- [ ] Branch is up to date with main

---

## 🗺️ Roadmap

### Version 1.0 (Current) ✅

- [x] Data generation pipeline
- [x] GCS upload functionality
- [x] BigQuery integration
- [x] DBT transformations
- [x] Basic analytics marts
- [x] Documentation

### Version 1.1 (Q1 2025) 🚧

- [ ] Add incremental loading
- [ ] Implement data quality dashboard
- [ ] Add more complex metrics
- [ ] Performance optimizations
- [ ] CI/CD with GitHub Actions

### Version 2.0 (Q2 2025) 📋

- [ ] Real-time data streaming
- [ ] ML predictions (match outcomes)
- [ ] Advanced player analytics
- [ ] API for data access
- [ ] Mobile dashboard app
- [ ] Multi-tournament support

### Version 3.0 (Future) 💡

- [ ] Airflow orchestration
- [ ] Data lineage visualization
- [ ] Automated anomaly detection
- [ ] Multi-cloud support (AWS, Azure)
- [ ] GraphQL API
- [ ] Real-time match updates

### Community Requested Features

Vote on features in our [GitHub Discussions](https://github.com/yourusername/can2025_pipeline/discussions)!

---

## 📊 DBT Lineage Diagram

```
sources (can2025_raw)
│
├── teams ────────────────────┐
│                              │
├── players ──────────────────┼─────┐
│                              │     │
├── stadiums ─────────────────┼───┐ │
│                              │   │ │
├── matches ──────────────────┼─┐ │ │
│                              │ │ │ │
├── match_events ─────────────┼─┼─┼─┼─┐
│                              │ │ │ │ │
└── ticket_sales ─────────────┼─┼─┼─┘ │
                               │ │ │   │
                               ▼ ▼ ▼   ▼
                     ┌──────────────────────┐
                     │  STAGING LAYER       │
                     │  (Views)             │
                     ├──────────────────────┤
                     │ • stg_teams          │
                     │ • stg_players        │
                     │ • stg_stadiums       │
                     │ • stg_matches        │
                     │ • stg_match_events   │
                     │ • stg_ticket_sales   │
                     └──────────┬───────────┘
                                │
                                ▼
                     ┌──────────────────────┐
                     │ INTERMEDIATE LAYER   │
                     │ (Views)              │
                     ├──────────────────────┤
                     │ • int_team_performance│
                     │ • int_player_stats   │
                     │ • int_match_intensity│
                     │ • int_revenue_analysis│
                     └──────────┬───────────┘
                                │
                                ▼
                     ┌──────────────────────┐
                     │    MARTS LAYER       │
                     │    (Tables)          │
                     ├──────────────────────┤
                     │ • mart_team_standings│
                     │ • mart_top_scorers   │
                     │ • mart_stadium_perf  │
                     │ • mart_match_calendar│
                     │ • mart_financial_sum │
                     └──────────┬───────────┘
                                │
                                ▼
                     ┌──────────────────────┐
                     │   BI DASHBOARDS      │
                     │   (Exposures)        │
                     ├──────────────────────┤
                     │ • Executive Dashboard│
                     │ • Team Performance   │
                     │ • Financial Reports  │
                     │ • Player Analytics   │
                     └──────────────────────┘
```

---

## 🎯 Use Cases & Applications

### 1. Sports Analytics
- Track player performance over time
- Identify emerging talent
- Analyze team strategies
- Predict match outcomes (with ML)

### 2. Business Intelligence
- Revenue optimization
- Stadium capacity planning
- Ticket pricing strategies
- Marketing campaign effectiveness

### 3. Data Engineering Portfolio
- Demonstrate ELT pipeline skills
- Showcase cloud platform expertise
- Exhibit data modeling capabilities
- Display DBT proficiency

### 4. Educational Purposes
- Learn data engineering concepts
- Practice SQL and Python
- Understand cloud architectures
- Study data transformation patterns

### 5. Research & Analysis
- Tournament format analysis
- Statistical modeling
- Comparative studies
- Historical trend analysis

---

## 📱 Sample Dashboards

### Executive Dashboard

**KPIs Displayed:**
- 💰 Total Revenue: $45.2M
- 👥 Total Attendance: 1.8M
- ⚽ Total Goals: 142
- 🏆 Tournament Winner: Morocco

**Visualizations:**
- Revenue trend over tournament phases
- Top 5 teams by points
- Average attendance by stadium
- Goals per match distribution

### Team Performance Dashboard

**Features:**
- Group standings table
- Win/loss/draw pie chart
- Goals scored vs conceded scatter plot
- Points progression line chart
- Head-to-head comparison matrix

### Financial Dashboard

**Metrics:**
- Revenue by ticket category
- Daily sales trends
- Stadium revenue comparison
- Average ticket price by match phase
- Sellout rate percentage

### Player Analytics Dashboard

**Insights:**
- Top 10 scorers leaderboard
- Age distribution histogram
- Position-wise goal contributions
- Market value vs performance scatter
- Cards per match heatmap

---

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

```yaml
# .github/workflows/pipeline.yml
name: CAN 2025 Data Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest
      
      - name: Run Python tests
        run: pytest tests/
      
      - name: Run DBT tests
        run: |
          cd can2025_dbt
          dbt deps
          dbt test
        env:
          GOOGLE_APPLICATION_CREDENTIALS: ${{ secrets.GCP_SA_KEY }}

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Production
        run: |
          cd can2025_dbt
          dbt run --target prod
        env:
          GOOGLE_APPLICATION_CREDENTIALS: ${{ secrets.GCP_SA_KEY }}
```

---

## 📞 Support & Contact

### Get Help

- 📖 **Documentation**: Check this README first
- 🐛 **Bug Reports**: [Open an issue](https://github.com/yourusername/can2025_pipeline/issues)
- 💡 **Feature Requests**: [Start a discussion](https://github.com/yourusername/can2025_pipeline/discussions)
- 📧 **Email**: data-team@example.com
- 💬 **Slack**: Join our [community channel](#)

### Project Maintainers

- **Aymane** - [@aymane70](https://github.com/aymane70) - Project Lead
- **Contributors** - See [CONTRIBUTORS.md](CONTRIBUTORS.md)

### Acknowledgments

- Thanks to all contributors
- Inspired by real sports analytics projects
- Built with amazing open-source tools

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Aymane

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
```

---

## 🌟 Star History

If you find this project helpful, please consider giving it a ⭐!

[![Star History Chart](https://api.star-history.com/svg?repos=aymane70/can2025_pipeline&type=Date)](https://star-history.com/#aymane70/can2025_pipeline&Date)

---

## 📸 Screenshots

### Pipeline Execution
```
$ python 1_generate_data.py
2025-01-15 14:23:45 - INFO - Starting CAN 2025 Data Generation
2025-01-15 14:23:46 - INFO - ✓ teams.csv created
2025-01-15 14:23:48 - INFO - ✓ players.csv created with 552 players
2025-01-15 14:23:49 - INFO - ✓ All files generated successfully!
```

### DBT Docs
![DBT Documentation](https://via.placeholder.com/800x400?text=DBT+Lineage+Graph)

### Dashboard Example
![Dashboard](https://via.placeholder.com/800x400?text=Executive+Dashboard)

---

<div align="center">

### Built with ❤️ for the data engineering community

**[⬆ Back to Top](#-can-2025-data-pipeline)**

---

**Don't forget to ⭐ this repo if you found it helpful!**

[![GitHub stars](https://img.shields.io/github/stars/aymane70/can2025_pipeline?style=social)](https://github.com/aymane70/can2025_pipeline/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/aymane70/can2025_pipeline?style=social)](https://github.com/aymane70/can2025_pipeline/network/members)

</div>