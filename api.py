from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.cloud import bigquery
from google.auth import default
import os

app = FastAPI()

# 環境変数から設定を取得
PROJECT_ID = os.environ.get("PROJECT_ID")
DATASET_ID = os.environ.get("BQ_DATASET_ID")
TABLE_NAME = os.environ.get("BQ_TABLE_NAME")

# 必要な環境変数が設定されているか確認
required_env_vars = {
    "GCP_PROJECT_ID": PROJECT_ID,
    "BQ_DATASET_ID": DATASET_ID,
    "BQ_TABLE_NAME": TABLE_NAME
}

for var_name, var_value in required_env_vars.items():
    if not var_value:
        raise ValueError(f"{var_name} environment variable is not set")

# ADCを使用してクレデンシャルを取得
credentials, project = default()

# BigQuery クライアントの設定
client = bigquery.Client(credentials=credentials, project=PROJECT_ID)

class InventoryRequest(BaseModel):
    customer_name: str
    store_name: str
    product_code: str

@app.post("/inventory")
async def get_inventory(request: InventoryRequest):
    query = f"""
    SELECT 
        customer_name,
        store_name,
        product_code,
        product_name,
        quantity,
        last_updated
    FROM 
        `{PROJECT_ID}.{DATASET_ID}.{TABLE_NAME}`
    WHERE 
        customer_name = @customer_name
        AND store_name = @store_name
        AND product_code = @product_code
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("customer_name", "STRING", request.customer_name),
            bigquery.ScalarQueryParameter("store_name", "STRING", request.store_name),
            bigquery.ScalarQueryParameter("product_code", "STRING", request.product_code),
        ]
    )

    try:
        query_job = client.query(query, job_config=job_config)
        results = query_job.result()

        if results.total_rows == 0:
            raise HTTPException(status_code=404, detail="Inventory data not found")

        inventory_data = next(results)
        
        return {
            "customer_name": inventory_data.customer_name,
            "store_name": inventory_data.store_name,
            "product_code": inventory_data.product_code,
            "product_name": inventory_data.product_name,
            "quantity": inventory_data.quantity,
            "last_updated": inventory_data.last_updated.isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
