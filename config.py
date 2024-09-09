import os
  
VERTEX_AI_LOCATION = "global"
PROJECT_ID = os.environ.get("PROJECT_ID")
DATASTORE_ID = os.environ.get("DATASTORE_ID")

BUCKET_NAME = os.environ.get("BUCKET_NAME", PROJECT_ID)
LOCATION = os.environ.get("LOCATION", "europe-west1")

BQ_PROJECT = os.environ.get("BQ_PROJECT_ID", PROJECT_ID)
BQ_DATASET = os.environ.get("BQ_DATASET_ID", "my_dataset")
BQ_TABLE = os.environ.get("BQ_TABLE_ID", "spanner_analysis")

SPANNER_DATABASE = os.environ.get("SPANNER_DATABASE_ID")
SPANNER_INSTANCE = os.environ.get("SPANNER_INSTANCE_ID")
