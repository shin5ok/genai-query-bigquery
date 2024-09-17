
BUCKET_NAME?=$(PROJECT_ID)


.PHONY: deploy
deploy:
	gcloud run deploy genai-query-api \
	--source=. \
	--region=asia-northeast1 \
	--cpu=1 \
	--memory=512M \
	--ingress=internal-and-cloud-load-balancing \
	--set-env-vars=PROJECT_ID=$(PROJECT_ID),BQ_DATASET_ID=$(BQ_DATASET_ID) \
	--min-instances=1 \
	--service-account=genai-query-api@$(PROJECT_ID).iam.gserviceaccount.com \
	--allow-unauthenticated

.PHONY: sa
sa:
	gcloud iam service-accounts create genai-query-api

.PHONY: iam
iam:
	gcloud projects add-iam-policy-binding $(PROJECT_ID) \
	--member=serviceAccount:genai-query-api@$(PROJECT_ID).iam.gserviceaccount.com \
	--role=roles/aiplatform.user

	gcloud projects add-iam-policy-binding $(PROJECT_ID) \
	--member=serviceAccount:genai-query-api@$(PROJECT_ID).iam.gserviceaccount.com \
	--role=roles/storage.objectUser

