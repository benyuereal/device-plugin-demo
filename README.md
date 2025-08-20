# device-plugin-demo
device-plugin


### 应用
```shell
kubectl apply -f deployment/qwen-mini.yaml
```

```shell
kubectl get pod 
kubectl describe pod -l app=qwen 
kubectl logs -f -l app=qwen
kubectl delete pod -l app=qwen
kubectl delete deployment qwen-mini
```