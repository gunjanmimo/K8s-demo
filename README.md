# METHINKSAI



Endpoint:




### USEFUL COMMANDS 

Setup kubectl with AKS 

```
az login 

az aks get-credentials --resource-group methinksAI --name backend-deployment-cluster

# GENERATE AZURE CREDENTIAL FOR GITHUB ACTION 
```



Deployment 

```
cd path_to_methinksAI-assignment_dir

kubectl apply -f k8s/database_service
kubectl apply -f k8s/backend_service
```