# device-plugin-demo
device-plugin


### 应用
```shell
kubectl apply -f deployment/qwen-mini.yaml
kubectl apply -f deployment/gpu-test.yaml
kubectl apply -f deployment/kuda-test.yaml

```

```shell
kubectl get pod 
kubectl describe pod -l app=qwen 
kubectl logs -f -l app=qwen
kubectl delete pod -l app=qwen
kubectl delete deployment qwen-mini
kubectl delete statefulset qwen-mini

kubectl exec -it qwen-mini-0 -- sh

kubectl logs -f pod cuda-test
kubectl logs -f -l app=qwen

```