### 切片实现gpu虚拟出多个
#### 启用配置

##### 启用配置
```shell
kubectl apply -f nvidia-device-plugin-daemonset.yaml 
```

##### 
##### 删除配置
```shell
kubectl delete pod -n kube-system -l name=nvidia-device-plugin-ds
```

##### 查看新的pod
```shell
kubectl get pod -n kube-system -l name=nvidia-device-plugin-ds

```