# Criando uma nova function a partir de um template pré-definido.
A seguir um passo a passo como sobre efetuar a criação e configuração inicial de uma cloud function.

Atente-se ao tópico de Observações Importantes (https://github.com/dougsaraiva/deploy-cloud-function/edit/develop/README.md#observa%C3%A7%C3%B5es-importantes)


## Instalação do cookiecutter
Cookiecutter fornece uma estrutura básica com arquivos e diretórios predefinidos.

```
 pip install cookiecutter
```

## Criação do template
- **template_gcs**: 
O template_gcs é um modelo de Google Cloud Functions que é usado para criar uma função que é acionada por eventos de armazenamento no Google Cloud Storage (GCS).

```
 cookiecutter template_gcs
```

- **template_http**:
O template_http é um modelo de Google Cloud Functions que é usado para criar uma função que é acionada por solicitações HTTP.

```
 cookiecutter template_http
```

### Configurações para todos os tipos de templates
Ao efetuar a execução da linha de comando sobre qualquer um dos templates referidos acima, será necessário preencher as seguintes informações a seguir:

- **google_function_name [e.g. 'google_function_name']**: Essa variável é usada para definir o nome da função que será criada.
- **entry_point [e.g. 'hello_world']:** Aqui você deve fornecer o ponto de entrada da sua função, será o metodo responsável por inicar a chamada de todo o código.
- **memory:** Essa variável define as opções de memória disponíveis para a sua função no Google Cloud Functions. Ela é uma lista que contém diferentes valores de memória em megabytes (MB), por padrão 256MB.
- **timeout:** Essa variável define as opções de tempo limite disponíveis para a sua função no Google Cloud Functions, onde o máximo por padrão são 540s
- **min_auto_scaling_instances (MÍNIMO 0):** Essa variável define o número mínimo de instâncias que serão escaladas automaticamente para lidar com a carga de trabalho da função.
- **max_auto_scaling_instances (MÁXIMO 3000):** Essa variável define o número máximo de instâncias que serão escaladas automaticamente para lidar com a carga de trabalho da função
- **runtime:** Essa variável define as opções de tempo de execução disponíveis para a sua função no Google Cloud Functions. Ela é uma lista que contém diferentes versões do Python disponíveis.

### Configurações específicas por template 
### template_gcs
- **event_trigger_type:** Especifica qual ação voltada ao Google Cloud Storage deve acionar a função

  1.**google.storage.object.finalize**: Ao (finalizar/criar) arquivo no bucket selecionado

- **event_trigger_resource [e.g. 'dp-c360-XXX']** Especifica qual o bucket deve ser observado. Quando o evento especificado ocorre no recurso observado, a função é acionada e executada

# Observações Importantes
Dentro do dirétorio de cada template criado possuimos alguns arquivos que devem ser utilizados em determinadas fases do desenvolvimento: 

## gcloud_functions_deploy.sh
 O arquivo gcloud_functions_deploy contém um comando utilizado para implantar (deploy) uma função do Google Cloud Functions, recomenda-se ser utilizada para intuitos de testes no ambiente desenvolvimento, para executa-lo é necessário:

1. Abra o terminal no Visual Code.
2. Navegue até o diretório onde o arquivo gcloud_functions_deploy.sh está localizado, **substitua [nome da google function] pelo nome do diretório***: 

```
 cd [nome da google function]
``` 

3. Certifique-se de que o arquivo tenha permissão de execução:

```bash
 chmod +x gcloud_functions_deploy.sh
``` 
4. Execute o arquivo gcloud_functions_deploy.sh usando o comando:

```bash
 ./gcloud_functions_deploy.sh
``` 
## parameters.yaml
Ele será utilizado para compor o arquivo que irá efetuar a orquestração do deploy no ambiente do Github.

1. Certifique-se que encontra-se no diretório padrão "" e execute o código no terminal a seguir no terminal:
**Substitua [nome da google function] pelo nome do diretório.**
```
cat config.yml [nome da google function]/parameters.yml > .github/workflows/[nome da google function].yml
```


2. Após a execução verifique se foi efetuada a criacão de um novo arquivo no caminho referido na linha de comando acima (.github/workflows/), acesse o arquivo e em paths mencione o nome/diretório onde encontra-se os arquivos inerente a cloud function a ser implementada, **substitua [nome da google function] pelo nome do diretório.**


```
on:
  pull_request:
    branches:
      - 'main'
      - 'develop'
    types:
      - closed
       
    paths:
      - '[nome da google function]/**'
```

## requirements.txt
O arquivo requirements.txt é comumente para especificar as dependências do projeto. No contexto de uma função do Google Cloud, o arquivo requirements.txt é usado para listar as bibliotecas Python que a função precisa para ser executada corretamente.

Exemplo de preenchimento:

```
# package>=version
google-cloud-storage
google-cloud-bigquery
datetime
pytz
```


