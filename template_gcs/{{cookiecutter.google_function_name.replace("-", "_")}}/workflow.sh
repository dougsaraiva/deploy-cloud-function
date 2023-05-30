cat config.yml {{cookiecutter.google_function_name.replace("-","_")}}/parameters.yaml > .github/workflows/cloud_functions_deploy_{{cookiecutter.google_function_name.replace("-","_")}}.yml
