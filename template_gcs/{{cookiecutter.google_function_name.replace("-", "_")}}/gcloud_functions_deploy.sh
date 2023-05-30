gcloud functions deploy {{cookiecutter.google_function_name.replace("-", "_")}} \
  --entry-point {{cookiecutter.entry_point}} \
  --runtime {{cookiecutter.runtime}} \
  --region {{cookiecutter.region}} \
  --trigger-http \
  --memory '{{((cookiecutter.memory.replace("MB","")).replace("(default)","")).replace(" ", "")}}' \
  --timeout '{{(cookiecutter.timeout.replace("(default)","")).replace(" ", "")}}' \
  --min-instances {{cookiecutter.min_auto_scaling_instances}} \
  --max-instances {{cookiecutter.max_auto_scaling_instances}} \
  --trigger-event {{cookiecutter.event_trigger_type}} \
  --trigger-resource {{cookiecutter.event_trigger_resource}}