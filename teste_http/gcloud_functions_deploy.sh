gcloud functions deploy teste_http \
  --entry-point hello_world \
  --runtime python311 \
  --region us-east1 \
  --trigger-http \
  --memory '128' \
  --timeout '30s' \
  --min-instances 0 \
  --max-instances 1000