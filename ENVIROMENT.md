
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
minikube start --driver=docker --gpus=nvidia --container-runtime=docker
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

