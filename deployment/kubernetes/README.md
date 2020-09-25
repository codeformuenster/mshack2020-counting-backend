# Deployment

## Initial deployment

```
kubectl create ns mshack2020
kustomize build | kubectl apply -f -
```

## Deployment after changes to master

Change the image tag in the `kustomization.yaml` `images` section.

```
kustomize build | kubectl apply -f -
```

### Optional: For changed database schema

Do this before `apply`

```
kubectl -n mshack2020 delete statefulsets/postgres pvc/data-postgres-0
```
