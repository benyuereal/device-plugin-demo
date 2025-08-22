# device-plugin-demo
device-plugin


### 应用
```shell
kubectl apply -f deployment/qwen-mini.yaml
kubectl apply -f deployment/gpu-test.yaml
kubectl apply -f deployment/kuda-test.yaml
kubectl apply -f deployment/microgpu-test-pod.yaml
kubectl apply -f deployment/microgpu-test.yaml

```

```shell
kubectl get pod 
kubectl describe pod -l app=qwen 
kubectl logs -f -l app=qwen
kubectl delete pod -l app=qwen
kubectl delete pod qwen-mini-0 --force --grace-period=0
kubectl delete deployment qwen-mini
kubectl delete statefulset qwen-mini

kubectl exec -it qwen-mini-0 -- sh

kubectl logs -f pod cuda-test
kubectl logs -f -l app=qwen
kubectl exec -it qwen-mini-0 -- bash
kubectl delete pod microgpu-test-pod

kubectl get pod microgpu-test -w
kubectl describe pod -l microgpu-test
kubectl delete pod microgpu-test

kubectl logs microgpu-test -f

# 检查CUDA
nvidia-smi
ls -l /usr/local/cuda

# 检查PyTorch
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"

# 检查bitsandbytes
python -c "import bitsandbytes; print(bitsandbytes.__version__)"

docker run --runtime=nvidia \
    -e NVIDIA_VISIBLE_DEVICES=MIG-08d99649-629b-5eef-99c2-513890a668e0 \
    nvidia/cuda nvidia-smi

```