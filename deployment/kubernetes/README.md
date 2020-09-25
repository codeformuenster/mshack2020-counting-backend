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
