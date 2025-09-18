
# Spotify ETL Pipeline: AWS S3 + Lambda + Snowflake

## Overview
This project builds an **end-to-end ETL pipeline** that extracts data from the **Spotify API**, stores raw data in **AWS S3**, processes it using **AWS Lambda**, and automatically loads the transformed data into **Snowflake** using **Snowpipe** for analytics.

### Key Features
- Spotify API → AWS S3 → Lambda → Snowflake
- Automated data ingestion and transformation
- Scalable cloud-based data warehouse (Snowflake)
- End-to-end orchestration using AWS services

---

## Architecture

<img width="732" height="413" alt="image" src="https://github.com/user-attachments/assets/cd26489d-aa7b-48d6-8a32-ea8a92507dd4" />

```
Spotify API
    │
    ▼
AWS S3 (Raw Zone) ──► AWS Lambda (Transform) ──► AWS S3 (Curated Zone) ──► Snowpipe ──► Snowflake Tables
```

- **Raw Zone:** Stores raw JSON payloads from Spotify
- **Curated Zone:** Stores cleaned CSV files for songs, albums, and artists
- **Snowpipe:** Automatically ingests curated files into Snowflake tables
- **Snowflake:** Runs analytics queries with optimized schemas

---

## Tech Stack

| Component        | Technology Used               |
|------------------|-------------------------------|
| Data Source       | Spotify Web API               |
| Ingestion         | Python, Spotipy, AWS S3        |
| Transformation    | AWS Lambda (Python)           |
| Storage           | AWS S3 (Raw + Curated)         |
| Data Warehouse    | Snowflake                     |
| Automation        | Terraform (AWS Infra)         |
| Visualization     | Snowflake Worksheets, BI Tools |

---

## Folder Structure

```
spotify-etl-pipeline/
│
├── extractor/            # Spotify API extraction code
│
├── lambda_transform/      # AWS Lambda transformation code
│
├── infra/                 # Terraform scripts for AWS
│
├── snowflake/              # SQL scripts for Snowflake
│
├── requirements.txt        # Python dependencies
│
├── README.md               # Project documentation
│
└── .env                    # Environment variables (local only)
```

---

## Prerequisites

- **Spotify Developer App**  
  - Get `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET` from the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).  

- **AWS Account**  
  - Must have permissions for S3, Lambda, and IAM.  

- **Snowflake Account**  
  - Requires permissions to create Database, Schema, Stage, and Snowpipe.  

- **Terraform Installed**  
  - MacOS: `brew install terraform`  
  - Windows: `choco install terraform`  

---

## Setup Instructions

### 1. Clone Repository
```bash
git clone <repo-url>
cd spotify-etl-pipeline
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables  
Create a `.env` file:
```env
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_PLAYLIST_ID=your_playlist_id
S3_BUCKET=spotify-etl-pipeline-demo
AWS_REGION=us-east-1
```

---

## Deployment

### 1. Deploy AWS Infrastructure (Terraform)
```bash
cd infra
terraform init
terraform apply
```
This creates:  
- S3 bucket  
- Lambda IAM role & permissions  
- Lambda function  
- S3 → Lambda trigger  

---

### 2. Deploy Lambda Code
```bash
cd ../lambda_transform
zip -r ../infra/lambda_transform.zip .
```
Re-run `terraform apply` if needed after adding the Lambda zip file.

---

### 3. Run Extractor
```bash
cd ../extractor
python extract_playlist.py
```
This uploads raw playlist JSON to S3.  
S3 event → triggers Lambda → writes curated CSVs → Snowpipe auto-ingests into Snowflake tables.

---

## Snowflake Setup

Run SQL scripts in order:
```sql
-- 1) Create DB & schema
!source snowflake/01_create_db_schema.sql

-- 2) Create tables
!source snowflake/02_create_tables.sql

-- 3) Create stage & Snowpipe
!source snowflake/03_stage_snowpipe.sql
```

---

## Project Highlights

- **Serverless:** No servers to manage, fully event-driven  
- **Infrastructure as Code:** Reproducible AWS setup using Terraform  
- **Analytics-ready:** Snowflake tables with primary/foreign keys for BI dashboards  
- **Scalable:** Add more playlists or pipelines with minimal changes  
