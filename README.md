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
kubectl describe pod microgpu-test-pod
kubectl exec -it microgpu-test-pod -- sh

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


###

```shell
sudo vim /etc/containerd/config.toml


[plugins."io.containerd.grpc.v1.cri".containerd.runtimes]
  [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.nvidia]
    privileged_without_host_devices = false
    runtime_type = "io.containerd.runc.v2"
    [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.nvidia.options]
      BinaryName = "/usr/bin/nvidia-container-runtime"
      
      
      
 # 创建测试容器
kubectl run test-runtime --image=ubuntu --restart=Never \
  --runtime-class=nvidia -- sleep infinity

# 获取容器ID
CONTAINER_ID=$(sudo crictl ps -n test-runtime -q)

# 检查运行时类型
sudo crictl inspect $CONTAINER_ID | jq '.info.runtimeSpec.annotations'


#### 预期输出

{
  "io.kubernetes.cri.container-type": "CONTAINER",
  "io.kubernetes.cri-o.CgroupManager": "systemd",
  "io.kubernetes.cri-o.Devices": "/dev/nvidia0:/dev/nvidia0...", // 关键！
  "io.kubernetes.cri-o.Annotations": "..."
}

# 创建 GPU 测试容器
kubectl run gpu-test --image=nvcr.io/nvidia/cuda:12.3.0-base \
  --runtime-class=nvidia -- nvidia-smi

### 方法 4：验证挂载点注入
# 检查挂载点
kubectl logs gpu-test | grep -A 5 "Devices"


sudo ctr run --rm --runtime io.containerd.runtime.v1.linux \
  --gpus 0 \
  nvcr.io/nvidia/pytorch:24.05-py3 nvidia-test \
  nvidia-smi

nvcr.io/nvidia/pytorch:24.05-py3

docker pull nvidia/cuda:12.4.0-base-ubuntu22.04
```