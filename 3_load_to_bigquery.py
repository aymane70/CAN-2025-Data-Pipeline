# =============================================================================
# lambarki aymane 
# github.com/aymane70
# =============================================================================

import os
import json
import logging
from datetime import datetime
from google.cloud import bigquery
from google.cloud.exceptions import NotFound
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()


os.makedirs('logs', exist_ok=True)


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/bigquery_load.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)



PROJECT_ID = os.getenv("PROJECT_ID") 
DATASET_ID = os.getenv("DATASET_ID") 
BUCKET_NAME = os.getenv("BUCKET_NAME") 
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE") 

GCS_PREFIX = "raw_data/"  
UPLOAD_DATE = datetime.now().strftime('%Y%m%d')  


TABLE_CONFIGS = {
    'teams': {
        'file_pattern': f"raw_data/{UPLOAD_DATE}/teams/teams.csv",  # Fixed path
        'schema': [
            bigquery.SchemaField("team_id", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("team_name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("group_name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("fifa_ranking", "INTEGER"),
            bigquery.SchemaField("coach_name", "STRING"),
            bigquery.SchemaField("coach_nationality", "STRING"),
        ]
    },
    'players': {
        'file_pattern': f"raw_data/{UPLOAD_DATE}/players/players.csv",
        'schema': [
            bigquery.SchemaField("player_id", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("team_id", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("player_name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("position", "STRING"),
            bigquery.SchemaField("age", "INTEGER"),
            bigquery.SchemaField("height_cm", "INTEGER"),
            bigquery.SchemaField("club", "STRING"),
            bigquery.SchemaField("market_value_millions", "FLOAT"),
        ]
    },
    'stadiums': {
        'file_pattern': f"raw_data/{UPLOAD_DATE}/stadiums/stadiums.csv",
        'schema': [
            bigquery.SchemaField("stadium_id", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("stadium_name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("city", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("capacity", "INTEGER"),
        ]
    },
    'matches': {
        'file_pattern': f"raw_data/{UPLOAD_DATE}/matches/matches.csv",
        'schema': [
            bigquery.SchemaField("match_id", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("match_date", "DATE", mode="REQUIRED"),
            bigquery.SchemaField("stadium_id", "INTEGER"),
            bigquery.SchemaField("home_team_id", "INTEGER"),
            bigquery.SchemaField("away_team_id", "INTEGER"),
            bigquery.SchemaField("home_score", "INTEGER"),
            bigquery.SchemaField("away_score", "INTEGER"),
            bigquery.SchemaField("attendance", "INTEGER"),
            bigquery.SchemaField("round", "STRING"),
            bigquery.SchemaField("status", "STRING"),
        ]
    },
    'match_events': {
        'file_pattern': f"raw_data/{UPLOAD_DATE}/match_events/match_events.csv",
        'schema': [
            bigquery.SchemaField("event_id", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("match_id", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("player_id", "INTEGER"),
            bigquery.SchemaField("event_type", "STRING"),
            bigquery.SchemaField("minute", "INTEGER"),
            bigquery.SchemaField("team_id", "INTEGER"),
        ]
    },
    'ticket_sales': {
        'file_pattern': f"raw_data/{UPLOAD_DATE}/ticket_sales/ticket_sales.csv",
        'schema': [
            bigquery.SchemaField("sale_id", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("match_id", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("sale_date", "DATE"),
            bigquery.SchemaField("ticket_category", "STRING"),
            bigquery.SchemaField("quantity", "INTEGER"),
            bigquery.SchemaField("price_usd", "INTEGER"),
            bigquery.SchemaField("total_revenue", "INTEGER"),
        ]
    }
}

def get_bigquery_client():
    """Initialize BigQuery client with service account authentication"""
    try:
        if os.path.exists(SERVICE_ACCOUNT_FILE):
            credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE,
                scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
            logger.info(f"✓ Using service account from: {SERVICE_ACCOUNT_FILE}")
            
            client = bigquery.Client(
                project=PROJECT_ID,
                credentials=credentials
            )
            return client
        else:
            logger.info("⚠ Service account file not found, using default credentials")
            client = bigquery.Client(project=PROJECT_ID)
            return client
            
    except Exception as e:
        logger.error(f"✗ Failed to initialize BigQuery client: {str(e)}")
        return None

def discover_gcs_files():
    """Discover actual GCS files (in case date is different)"""
    logger.info("\n🔍 Discovering GCS files...")
    
    try:
        from google.cloud import storage
        
        if os.path.exists(SERVICE_ACCOUNT_FILE):
            credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE
            )
            storage_client = storage.Client(credentials=credentials, project=PROJECT_ID)
        else:
            storage_client = storage.Client(project=PROJECT_ID)
        
        bucket = storage_client.bucket(BUCKET_NAME)
        blobs = list(bucket.list_blobs(prefix="raw_data/"))
        
        if not blobs:
            logger.warning("⚠ No files found in raw_data/ folder")
            return {}
        
        
        date_folders = set()
        for blob in blobs:
            parts = blob.name.split('/')
            if len(parts) >= 2 and parts[1].isdigit() and len(parts[1]) == 8:
                date_folders.add(parts[1])
        
        if not date_folders:
            logger.error("❌ No date folders found in raw_data/")
            return {}
        
        
        latest_date = sorted(date_folders)[-1]
        logger.info(f"📅 Found date folders: {', '.join(sorted(date_folders))}")
        logger.info(f"📅 Using latest date: {latest_date}")
        
        
        updated_configs = {}
        for table_name, config in TABLE_CONFIGS.items():
            
            old_pattern = config['file_pattern']
            new_pattern = old_pattern.replace(UPLOAD_DATE, latest_date)
            config['file_pattern'] = new_pattern
            updated_configs[table_name] = config
            
            
            blob = bucket.blob(new_pattern)
            if blob.exists():
                size_mb = blob.size / (1024 * 1024)
                logger.info(f"  ✅ {table_name}: {new_pattern} ({size_mb:.1f} MB)")
            else:
                logger.warning(f"  ⚠ {table_name}: NOT FOUND at {new_pattern}")
        
        return updated_configs
        
    except Exception as e:
        logger.error(f"❌ Failed to discover GCS files: {str(e)}")
        return TABLE_CONFIGS  

def create_dataset_if_not_exists(client, dataset_id):
    """Create BigQuery dataset if it doesn't exist"""
    dataset_ref = f"{PROJECT_ID}.{dataset_id}"
    
    try:
        client.get_dataset(dataset_ref)
        logger.info(f"✅ Dataset {dataset_ref} already exists")
        return True
    except NotFound:
        try:
            logger.info(f"📊 Creating dataset {dataset_ref}...")
            dataset = bigquery.Dataset(dataset_ref)
            dataset.location = "US"
            dataset.description = "CAN 2025 Tournament Raw Data"
            dataset = client.create_dataset(dataset, timeout=30)
            logger.info(f"✅ Dataset {dataset_ref} created in region: US")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to create dataset {dataset_ref}: {str(e)}")
            return False

def load_table_from_gcs(client, table_name, config):
    """Load a single table from GCS to BigQuery"""
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
    gcs_uri = f"gs://{BUCKET_NAME}/{config['file_pattern']}"
    
    logger.info(f"\n📥 Loading {table_name}...")
    logger.info(f"  Source: {gcs_uri}")
    logger.info(f"  Destination: {table_id}")
    
    try:
        
        job_config = bigquery.LoadJobConfig(
            schema=config['schema'],
            skip_leading_rows=1,  
            source_format=bigquery.SourceFormat.CSV,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            autodetect=False,
        )
        
        
        load_job = client.load_table_from_uri(
            gcs_uri,
            table_id,
            job_config=job_config
        )
        
        logger.info(f"  ⏳ Job started: {load_job.job_id}")
        
        
        load_job.result()
        
        
        if load_job.error_result:
            logger.error(f"  ❌ Job failed: {load_job.error_result}")
            return False
        
        
        table = client.get_table(table_id)
        logger.info(f"  ✅ Loaded {table.num_rows:,} rows")
        logger.info(f"  📊 Table size: {table.num_bytes / (1024*1024):.1f} MB")
        
        return True
            
    except Exception as e:
        logger.error(f"  ❌ Failed to load {table_name}: {str(e)}")
        return False

def load_all_tables():
    """Load all tables from GCS to BigQuery"""
    logger.info("=" * 60)
    logger.info("🚀 Starting BigQuery Data Load")
    logger.info("=" * 60)
    
    
    if os.path.exists(SERVICE_ACCOUNT_FILE):
        with open(SERVICE_ACCOUNT_FILE, 'r') as f:
            sa_info = json.load(f)
            logger.info(f"🔑 Service Account: {sa_info.get('client_email')}")
    
    logger.info(f"📁 Project: {PROJECT_ID}")
    logger.info(f"🗄️  Dataset: {DATASET_ID}")
    logger.info(f"📦 Source bucket: {BUCKET_NAME}")
    
    
    client = get_bigquery_client()
    if not client:
        return False
    
    
    global TABLE_CONFIGS
    TABLE_CONFIGS = discover_gcs_files()
    if not TABLE_CONFIGS:
        logger.error("❌ No GCS files found to load")
        return False
    
    
    if not create_dataset_if_not_exists(client, DATASET_ID):
        return False
    
    
    success_count = 0
    failed_count = 0
    failed_tables = []
    
    for table_name, config in TABLE_CONFIGS.items():
        if load_table_from_gcs(client, table_name, config):
            success_count += 1
        else:
            failed_count += 1
            failed_tables.append(table_name)
    
    
    logger.info("=" * 60)
    logger.info("📊 Load Summary:")
    logger.info(f"  ✅ Successfully loaded: {success_count} tables")
    
    if failed_count > 0:
        logger.info(f"  ❌ Failed loads: {failed_count} tables")
        logger.info(f"  Failed tables: {', '.join(failed_tables)}")
    
    logger.info(f"  📍 Dataset location: {PROJECT_ID}.{DATASET_ID}")
    logger.info("=" * 60)
    
    return failed_count == 0

def verify_data():
    """Verify loaded data with sample queries"""
    logger.info("\n🔍 Verifying loaded data...")
    
    client = get_bigquery_client()
    if not client:
        return
    
    queries = {
        "Total teams": f"SELECT COUNT(*) as count FROM `{PROJECT_ID}.{DATASET_ID}.teams`",
        "Total players": f"SELECT COUNT(*) as count FROM `{PROJECT_ID}.{DATASET_ID}.players`",
        "Total matches": f"SELECT COUNT(*) as count FROM `{PROJECT_ID}.{DATASET_ID}.matches`",
        "Total events": f"SELECT COUNT(*) as count FROM `{PROJECT_ID}.{DATASET_ID}.match_events`",
        "Total goals": f"SELECT COUNT(*) as count FROM `{PROJECT_ID}.{DATASET_ID}.match_events` WHERE event_type = 'Goal'",
        "Total ticket sales": f"SELECT COUNT(*) as count FROM `{PROJECT_ID}.{DATASET_ID}.ticket_sales`",
    }
    
    for description, query in queries.items():
        try:
            query_job = client.query(query)
            result = query_job.result()
            for row in result:
                logger.info(f"  📈 {description}: {row.count:,}")
        except Exception as e:
            logger.error(f"  ❌ Query failed for {description}: {str(e)}")

if __name__ == "__main__":
   
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        logger.warning(f"⚠ Service account file not found: {SERVICE_ACCOUNT_FILE}")
        logger.info("Will try other authentication methods...")
    
    
    success = load_all_tables()
    
    if success:
        logger.info("\n🎉 All tables loaded successfully!")
        verify_data()
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ DATA PIPELINE COMPLETE!")
        logger.info("=" * 60)
        logger.info("\n📊 Next steps:")
        logger.info("1. Navigate to your DBT project: cd can2025_dbt")
        logger.info("2. Run DBT models: dbt run")
        logger.info("3. Test your models: dbt test")
        logger.info("4. Generate documentation: dbt docs generate && dbt docs serve")
        logger.info("\n🔗 BigQuery Console:")
        logger.info(f"   https://console.cloud.google.com/bigquery?project={PROJECT_ID}&p={PROJECT_ID}&d={DATASET_ID}")
        logger.info("=" * 60)
    else:
        logger.error("\n❌ Some tables failed to load")
        logger.error("\n🔧 Troubleshooting steps:")
        logger.error("1. Check if service account has BigQuery Admin permissions")
        logger.error(f"2. Verify files exist in GCS: gs://{BUCKET_NAME}/raw_data/")
        logger.error("3. Run this command to list files: gsutil ls gs://can_2025/raw_data/")
        logger.error("4. Check logs: logs/bigquery_load.log")
        exit(1)

