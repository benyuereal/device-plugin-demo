
### 单机环境下使用device plugin 部署模型

#### 一. 用户创建
##### 1. 临时切换回 root 用户
```shell
# 退出当前用户会话
exit
# 您应该会回到 root 用户提示符（root@G49218:~#）

```

##### 2. 赋予 k8sadmin 用户 sudo 权限
```shell
# 将用户添加到 sudo 组
sudo adduser k8sadmin
sudo usermod -aG docker k8sadmin
usermod -aG sudo k8sadmin
```

```shell
# 测试权限
sudo -u k8sadmin sudo -v
su - k8sadmin
```

##### 3. 安装 minikube
```shell
# 确保您在 root 用户下
# 应显示 /root
pwd  
# 重新安装 minikube
curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-amd64
# 安装 minikube
install minikube-linux-amd64 /usr/local/bin/minikube
```

##### 4. 配置用户权限
```shell
# 将用户添加到 docker 组以避免需要 sudo
usermod -aG docker k8sadmin

# 验证安装
sudo -u k8sadmin minikube version
```

##### 5. 切换回 k8sadmin 用户
```shell
   su - k8sadmin
# 现在您应该在 k8sadmin 用户下
```

##### 6. 启动 minikube（无需 sudo）
```shell
# 确保用户加入 docker 组
id | grep docker
```


#### 二. 启动集群
minikube start --driver=docker --gpus=nvidia --container-runtime=docker --image-repository=registry.aliyuncs.com/google_containers

```shell

minikube start \
  --driver=docker \
  --gpus=nvidia \
  --container-runtime=docker \
  --base-image="file:///var/lib/minikube/images/kicbase_v0.0.47.tar" \
  --alsologtostderr -v=8
  
minikube start \
  --driver=docker \
  --gpus=nvidia \
  --container-runtime=docker \
  --image-repository=registry.aliyuncs.com/google_containers \
  --docker-env HTTP_PROXY=http://10.0.168.50:7890 \
  --docker-env HTTPS_PROXY=http://10.0.168.50:7890 \
  --alsologtostderr -v=8
  
  
  minikube start \
  --driver=docker \
  --gpus=nvidia \
  --container-runtime=docker \
  --image-repository=registry.aliyuncs.com/google_containers \
  --docker-env HTTP_PROXY=http://10.0.168.50:7890 \
  --docker-env HTTPS_PROXY=http://10.0.168.50:7890 \
  --alsologtostderr -v=8
  
###
  
```
##### 安装kubernetes
```shell
minikube start --driver=docker --gpus=nvidia --container-runtime=docker  --force
minikube start --driver=docker --container-runtime=containerd --force
```

##### 安装container toolkit
```shell
# 添加仓库
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

# 安装工具包
sudo apt update
sudo apt install -y nvidia-container-toolkit
sudo systemctl restart docker
```
### 手动设置
```shell

sudo cat /etc/apt/trusted.gpg.d/nvidia-key.asc | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/nvidia.gpg
   ls
  rm -rf nvidia-key.asc

```

```asc
-----BEGIN PGP PUBLIC KEY BLOCK-----

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
X7sqI6cXUDG4BjpS70ZRWF2x51ZTiq7DLTV/gGw2okfVjoWjzQY0ebrLd4IoNs80
lIHmXxa+JdwB6WupCUzKCKLcPsX/yPAmswPNGAuIMAv+PWhUUSMVtzOZldnlogGM
hbJ9UD2txFGGh9WoYc2vgX9KAaKryXcC6QMabv7JJU24HEJJDgbJEvtFM5PS8QMF
bXIZsYgICWpQXVChBbduXo9sD2TUDWYAniNaaw4LKxPRG+Ix4HAqkh1oNOLojO30
DO3r1/62FKE5/ykg3iSMTDR0iOES/leXCCIO9fRJT8+eucxyOQoY5ti7tjt1wm3H
nTB+Rz3E/E2qeLs2PN82aseccm1G06pmsMCUiWtmSV6HjdO2XufYprrGLSu0RrT3
sz5WHGUOY2iO40xHhSiXg3TcLZRpv30DQzxoUrx9Ff//rXLFznh+MksuvVD2roUR
BGz/en31FxAcBoex9nNraeOekbFen5b7Xrq9wnzM5xZvJN2QYB3vS0khz/ZgFyy5
444ALa9gwb29FZCfA4m59S2QoB8uPQGM+8gnusE6J8y4fvI59ugafidIkt86dZ3m
FsEME5XNmBGdNEo2flRVFfpG1IWds2Ba3IsdbYd9nzmbBW7/n0InVRDrIg==
=9QWY
-----END PGP PUBLIC KEY BLOCK-----

```
```shell
deb https://nvidia.github.io/libnvidia-container/stable/ubuntu18.04/$(ARCH) /
#deb https://nvidia.github.io/libnvidia-container/experimental/ubuntu18.04/$(ARCH) /
deb https://nvidia.github.io/nvidia-container-runtime/stable/ubuntu18.04/$(ARCH) /
#deb https://nvidia.github.io/nvidia-container-runtime/experimental/ubuntu18.04/$(ARCH) /
deb https://nvidia.github.io/nvidia-docker/ubuntu18.04/$(ARCH) /
```

#### 三. (可选)安装kubectl 
```shell
snap install kubectl --classic
```


#### 五.创建 NVIDIA GPU Device Plugin
```shell
kubectl create -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.14.1/nvidia-device-plugin.yml
```


#### 六.启动模型进行测试


##### 下载模型

```shell
sudo apt install -y git-lfs

git lfs install

git clone https://huggingface.co/Qwen/Qwen1.5-0.5B-Chat
```


##### 挂载
```shell
# 1. 在宿主机打包模型目录

cd /home/k8sadmin
tar cvzf qwen-model.tgz Qwen1.5-0.5B-Chat

minikube ssh "sudo mkdir -p /home/k8sadmin"

# 2. 复制压缩包到 Minikube
minikube cp qwen-model.tgz /home/k8sadmin/qwen-model.tgz

# 3. 在 Minikube 内部解压
minikube ssh "cd /home/k8sadmin && tar xzf qwen-model.tgz && rm qwen-model.tgz"

```

##### 模型启动测试
```shell
MINIKUBE_IP=$(minikube ip)
echo "服务地址：http://${MINIKUBE_IP}:30080"

curl http://${MINIKUBE_IP}:30080/health

curl http://192.168.49.2:30080:30080/health


http://192.168.49.2:30080




```


```shell
curl -X POST http://${MINIKUBE_IP}:30080/generate \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": "中国的首都是哪里？",
    "parameters": {
      "max_new_tokens": 50
    }
  }'
  
  curl -X POST http://192.168.49.2:30080/generate \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": "中国的首都是哪里？",
    "parameters": {
      "max_new_tokens": 50
    }
  }'
```

```shell
curl -X POST http://${MINIKUBE_IP}:30080/generate \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": "<|im_start|>system\n你是一个AI助手<|im_end|>\n<|im_start|>user\n请用简单的话解释量子计算<|im_end|>\n<|im_start|>assistant\n",
    "parameters": {
      "max_new_tokens": 150,
      "temperature": 0.7,
      "top_p": 0.9
    }
  }'
  
  curl -X POST http://192.168.49.2:30080/generate \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": "<|im_start|>system\n你是一个AI助手<|im_end|>\n<|im_start|>user\n请用简单的话解释量子计算<|im_end|>\n<|im_start|>assistant\n",
    "parameters": {
      "max_new_tokens": 150,
      "temperature": 0.7,
      "top_p": 0.9
    }
  }'
```

##### 预期效果
<img width="2660" height="1378" alt="image" src="https://github.com/user-attachments/assets/66394bf1-c342-461d-8fad-2ae167ea0e02" />

<img width="2660" height="1378" alt="image" src="https://github.com/user-attachments/assets/3fe83bfa-d326-4724-b9ec-16e3acf5a344" />

