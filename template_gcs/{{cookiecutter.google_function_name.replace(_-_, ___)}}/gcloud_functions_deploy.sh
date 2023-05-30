gcloud functions deploy {{cookiecutter.google_function_name.replace("-", "_")}} \
  --entry-point {{cookiecutter.entry_point}} \
  --runtime {{cookiecutter.runtime}} \
  --trigger-http \
  --memory 256 \
  --timeout '{{(cookiecutter.timeout.replace("(default)","")).replace(" ", "")}}' \
  --min-instances {{cookiecutter.min_auto_scaling_instances}} \
  --max-instances {{cookiecutter.max_auto_scaling_instances}}