# METHINKSAI



### SETUP 

##### STEP 1. CREATE .env FILE 

```
  # Postgres
  DB_ENGINE=django.db.backends.postgresql
  DB_HOST=***
  DB_PORT=5432
  DB_NAME=***
  DB_USER=***
  DB_PASSWORD=***
  

  # Azure
  AZURE_ACCOUNT_NAME=***
  AZURE_ACCOUNT_KEY=***
  AZURE_CONTAINER_NAME=***
  AZURE_STORAGE_CONNECTION_STRING=***
  AZURE_QUEUES_NAME=
```

**Note**: put the `.env` in root dir


##### STEP 2: RUN WITH DOCKER COMPOSE LOCALLY

```
sudo rm -rf db/
docker-compose build
docker-compose up
```


### ENDPOINT DETAIL

##### IMAGE UPLOAD ENDPOINT 

**endpoint** : /apis/upload/
**method**: POST

**request**
- Headers

    Content-Type: multipart/form-data

- Parameters
    
    image: The image file to be uploaded. This should be a file input.



**sample response**

```
{
    "id": 37,
    "original_image_url": "https://holamethinkstask.blob.core.windows.net/images/original/eccd5e89-ef9e-49bf-a6fc-78c9374b179d.jpeg",
    "processed_image_url": null,
    "status": "pending",
    "upload_time": "2024-06-10T15:13:51.837204Z",
    "processing_start_time": null,
    "processing_end_time": null
}
```


##### ALL IMAGE TASK DETAILS
**endpoint** : /apis/tasks/

**method**: GET

**sample response**
```
[
    {
        "id": 1,
        "original_image_url": "https://holamethinkstask.blob.core.windows.net/images/original/58575466-37a8-4807-aba3-3a33ea8a21bb.jpg",
        "processed_image_url": "https://holamethinkstask.blob.core.windows.net/images/processed/58575466-37a8-4807-aba3-3a33ea8a21bb_processed.jpg",
        "status": "completed",
        "upload_time": "2024-06-10T15:36:30.730933Z",
        "processing_start_time": "2024-06-10T15:36:35.579294Z",
        "processing_end_time": "2024-06-10T15:36:35.725134Z"
    },
    {
        "id": 2,
        "original_image_url": "https://holamethinkstask.blob.core.windows.net/images/original/997036b3-65c1-400b-ac19-003144ca65fe.jpg",
        "processed_image_url": "https://holamethinkstask.blob.core.windows.net/images/processed/997036b3-65c1-400b-ac19-003144ca65fe_processed.jpg",
        "status": "completed",
        "upload_time": "2024-06-10T15:36:45.348888Z",
        "processing_start_time": "2024-06-10T15:36:50.560316Z",
        "processing_end_time": "2024-06-10T15:36:50.958846Z"
    }
]

```


##### SPECIFIC IMAGE TASK DETAILS
**endpoint** : /apis/tasks/<task_id:int>

**method**: GET

**sample response**

```
{
    "id": 1,
    "original_image_url": "https://holamethinkstask.blob.core.windows.net/images/original/58575466-37a8-4807-aba3-3a33ea8a21bb.jpg",
    "processed_image_url": "https://holamethinkstask.blob.core.windows.net/images/processed/58575466-37a8-4807-aba3-3a33ea8a21bb_processed.jpg",
    "status": "completed",
    "upload_time": "2024-06-10T15:36:30.730933Z",
    "processing_start_time": "2024-06-10T15:36:35.579294Z",
    "processing_end_time": "2024-06-10T15:36:35.725134Z"
}
```

### CI/CD PIPELINE 

**Pipeline Overview**
The pipeline is triggered by events:

- A push to the main branch.

**Permissions**

The pipeline requires write permissions to the repository contents.

**Jobs**

The pipeline consists of the following jobs:


1. Build
2. Test
3. Security
4. Merge

    - Runs on: ubuntu-latest
    - Needs: build, test, security
    - Steps:
        
        - Checks out the code from the repository.
        - Configures Git with GitHub Actions credentials.
        - Merges the code from the pull request to the main branch.
        - Authenticates with GitHub and pushes the merged code to the main branch.
5. Docker Push

    - Runs on: ubuntu-latest
    - Needs: merge
    - Steps:
        - Checks out the code from the repository.
        - Builds a Docker image for the Django application.
        - Logs in to Docker Hub using the provided credentials.
        - Pushes the Docker image to Docker Hub.


6. Deploy
    - Runs on: ubuntu-latest
    - Needs: docker-push
    - Steps:

        - Azure CLI login
        - Setup Kubectl 




GITHUB ACTION SECRET

- GH_TOKEN: GitHub token for authentication.
- DOCKER_USERNAME: Docker Hub username.
- DOCKER_PASSWORD: Docker Hub password.
- AZURE_CREDENTIAL: Azure cli authentication.
- AZURE_RESOURCE_GROUP: Azure resource group name.
- AZURE_AKS_CLUSTER_NAME: Azure AKS cluster name




### MANUAL DEPLOYMENT 


```
az login 

az aks get-credentials --resource-group methinksAI --name backend-deployment-cluster

docker build -t DOCKER_USERNAME/django-app:latest .
docker push DOCKER_USERNAME/django-app:latest

kubectl apply -f k8s/backend_service/.
kubectl apply -f k8s/database_service/.
```


