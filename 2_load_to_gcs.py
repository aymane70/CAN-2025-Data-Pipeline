# =============================================================================
# lambarki aymane 
# github.com/aymane70
# =============================================================================

import os
import json
import logging
from google.cloud import storage
from google.oauth2 import service_account
from datetime import datetime



os.makedirs('logs', exist_ok=True)


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/gcs_upload.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)




PROJECT_ID = os.getenv("PROJECT_ID")     
BUCKET_NAME = os.getenv("BUCKET_NAME") 
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE") 
LOCAL_DATA_DIR = os.getenv("LOCAL_DATA_DIR") 
GCS_PREFIX = "raw_data/"  


CSV_FILES = [
    'teams.csv',
    'players.csv',
    'stadiums.csv',
    'matches.csv',
    'match_events.csv',
    'ticket_sales.csv'
]

def load_service_account_key():
    """Load service account credentials from JSON file"""
    try:
        if os.path.exists(SERVICE_ACCOUNT_FILE):
            credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE,
                scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
            logger.info(f"✓ Loaded service account from: {SERVICE_ACCOUNT_FILE}")
            
            
            global PROJECT_ID
            if not PROJECT_ID and hasattr(credentials, 'project_id'):
                PROJECT_ID = credentials.project_id
                logger.info(f"✓ Using project ID from service account: {PROJECT_ID}")
            
            return credentials
        else:
            logger.warning(f"⚠ Service account file not found: {SERVICE_ACCOUNT_FILE}")
            logger.info("Falling back to GOOGLE_APPLICATION_CREDENTIALS environment variable")
            return None
    except Exception as e:
        logger.error(f"✗ Failed to load service account key: {str(e)}")
        return None

def get_storage_client():
    """Initialize GCS client with service account authentication"""
    try:
       
        credentials = load_service_account_key()
        
        if credentials:
            
            client = storage.Client(
                project=PROJECT_ID,
                credentials=credentials
            )
            logger.info("✓ Authenticated using service account JSON file")
        else:
            
            client = storage.Client(project=PROJECT_ID)
            logger.info("✓ Authenticated using default credentials")
        
        return client
        
    except Exception as e:
        logger.error(f"✗ Failed to initialize GCS client: {str(e)}")
        logger.error("\nAuthentication methods tried:")
        logger.error("1. Service account file: service-account-key.json")
        logger.error("2. GOOGLE_APPLICATION_CREDENTIALS environment variable")
        logger.error("3. Default application credentials")
        return None

def create_bucket_if_not_exists(storage_client, bucket_name):
    """Create GCS bucket if it doesn't exist"""
    try:
        bucket = storage_client.get_bucket(bucket_name)
        logger.info(f"✓ Bucket {bucket_name} already exists")
        return bucket
    except Exception:
        try:
            logger.info(f"Creating bucket {bucket_name}...")
            bucket = storage_client.create_bucket(bucket_name, location="US")
            logger.info(f"✓ Bucket {bucket_name} created in region: US")
            
            
            policy = bucket.get_iam_policy(requested_policy_version=3)
            
            logger.info(f"✓ Bucket created with private access (no public access)")
            return bucket
        except Exception as e:
            logger.error(f"✗ Failed to create bucket {bucket_name}: {str(e)}")
            raise

def upload_file_to_gcs(bucket, local_file_path, gcs_blob_name):
    """Upload a single file to GCS"""
    try:
        
        file_size = os.path.getsize(local_file_path)
        
        
        blob = bucket.blob(gcs_blob_name)
        
        
        logger.info(f"📤 Uploading {os.path.basename(local_file_path)} ({file_size:,} bytes)...")
        blob.upload_from_filename(local_file_path)
        
        
        blob.reload()
        if blob.exists():
            logger.info(f"✅ Uploaded to gs://{bucket.name}/{gcs_blob_name}")
            return True
        else:
            logger.error(f"✗ Upload verification failed for {gcs_blob_name}")
            return False
            
    except Exception as e:
        logger.error(f"✗ Failed to upload {local_file_path}: {str(e)}")
        return False

def upload_all_csv_files():
    """Upload all CSV files to GCS"""
    logger.info("=" * 60)
    logger.info("Starting upload to Google Cloud Storage")
    logger.info(f"Project: {PROJECT_ID}")
    logger.info(f"Bucket: {BUCKET_NAME}")
    logger.info("=" * 60)
    
    
    if os.path.exists(SERVICE_ACCOUNT_FILE):
        with open(SERVICE_ACCOUNT_FILE, 'r') as f:
            sa_info = json.load(f)
            logger.info(f"Service Account: {sa_info.get('client_email')}")
    
    
    storage_client = get_storage_client()
    if not storage_client:
        return False
    
    
    try:
        bucket = create_bucket_if_not_exists(storage_client, BUCKET_NAME)
    except Exception as e:
        logger.error(f"✗ Failed to access bucket: {str(e)}")
        return False
    
    
    upload_count = 0
    failed_count = 0
    skipped_count = 0
    
    logger.info("\n📁 Uploading files:")
    for csv_file in CSV_FILES:
        local_path = os.path.join(LOCAL_DATA_DIR, csv_file)
        
        if not os.path.exists(local_path):
            logger.warning(f"⚠ File not found, skipping: {csv_file}")
            skipped_count += 1
            continue
        
        
        timestamp = datetime.now().strftime('%Y%m%d')
        file_base = os.path.splitext(csv_file)[0]
        gcs_blob_name = f"{GCS_PREFIX}{timestamp}/{file_base}/{csv_file}"
        
        if upload_file_to_gcs(bucket, local_path, gcs_blob_name):
            upload_count += 1
        else:
            failed_count += 1
    
    
    logger.info("=" * 60)
    logger.info("📊 Upload Summary:")
    logger.info(f"  ✅ Successfully uploaded: {upload_count} files")
    logger.info(f"  ⚠ Skipped (not found): {skipped_count} files")
    logger.info(f"  ❌ Failed uploads: {failed_count} files")
    logger.info(f"  🗂️  Bucket location: gs://{BUCKET_NAME}/{GCS_PREFIX}")
    logger.info("=" * 60)
    
    return failed_count == 0

def list_bucket_contents():
    """List all files in the GCS bucket"""
    try:
        storage_client = get_storage_client()
        if not storage_client:
            return
        
        bucket = storage_client.bucket(BUCKET_NAME)
        blobs = bucket.list_blobs(prefix=GCS_PREFIX)
        
        logger.info("\n📂 Files in bucket:")
        file_count = 0
        for blob in blobs:
            size_mb = blob.size / (1024 * 1024)
            updated = blob.updated.strftime('%Y-%m-%d %H:%M') if blob.updated else 'N/A'
            logger.info(f"  ├─ {blob.name}")
            logger.info(f"  │   Size: {size_mb:.2f} MB | Updated: {updated}")
            file_count += 1
        
        if file_count == 0:
            logger.info("  └─ (No files found)")
        else:
            logger.info(f"  └─ Total: {file_count} files")
            
    except Exception as e:
        logger.error(f"Failed to list bucket contents: {str(e)}")

def check_local_files():
    """Check which local files exist"""
    logger.info("\n🔍 Checking local files:")
    existing_files = []
    missing_files = []
    
    for csv_file in CSV_FILES:
        local_path = os.path.join(LOCAL_DATA_DIR, csv_file)
        if os.path.exists(local_path):
            size = os.path.getsize(local_path)
            existing_files.append((csv_file, size))
        else:
            missing_files.append(csv_file)
    
    if existing_files:
        logger.info("✅ Found files:")
        for file_name, size in existing_files:
            size_kb = size / 1024
            logger.info(f"  ├─ {file_name} ({size_kb:.1f} KB)")
    
    if missing_files:
        logger.info("❌ Missing files:")
        for file_name in missing_files:
            logger.info(f"  ├─ {file_name}")
    
    return len(existing_files) > 0

if __name__ == "__main__":
    
    if not os.path.exists(LOCAL_DATA_DIR):
        logger.error(f"✗ Local data directory not found: {LOCAL_DATA_DIR}")
        logger.error("Please run 1_generate_data.py first")
        exit(1)
    
    
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        logger.warning(f"⚠ Service account file not found: {SERVICE_ACCOUNT_FILE}")
        logger.info("Will try other authentication methods...")
        logger.info("\nTo use service account authentication:")
        logger.info("1. Download JSON key from GCP Console")
        logger.info("2. Save it as 'service-account-key.json' in current directory")
        logger.info("3. Or set GOOGLE_APPLICATION_CREDENTIALS environment variable")
    
    
    has_files = check_local_files()
    if not has_files:
        logger.error("\n✗ No CSV files found to upload")
        logger.error("Please run 1_generate_data.py first to generate data")
        exit(1)
    
    
    success = upload_all_csv_files()
    
    if success:
        logger.info("\n🎉 All files uploaded successfully!")
        list_bucket_contents()
    else:
        logger.error("\n❌ Some files failed to upload")
        exit(1)

