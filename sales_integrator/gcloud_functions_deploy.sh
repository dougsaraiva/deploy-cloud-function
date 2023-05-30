gcloud functions deploy sales_integrator \
  --entry-point read_gcs \
  --runtime python311 \
  --memory 256 \
  --timeout '60s' \
  --min-instances 0 \
  --max-instances 1000 \
  --trigger-event google.storage.object.finalize \
  --trigger-resource projects/_/buckets/dp-c360-dev-data-lake