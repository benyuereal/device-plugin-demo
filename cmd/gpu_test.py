import torch
import time
import numpy as np
from datetime import datetime

def gpu_stress_test(duration_sec=30, matrix_size=8000):
    """执行GPU压力测试并监控利用率"""
    # 验证CUDA可用性
    if not torch.cuda.is_available():
        print("错误：未检测到CUDA设备！")
        return

    device = torch.device('cuda')
    print(f"=== CUDA压力测试开始 ===")
    print(f"设备: {torch.cuda.get_device_name(0)}")
    print(f"CUDA版本: {torch.version.cuda}")
    print(f"PyTorch版本: {torch.__version__}")
    print(f"测试时长: {duration_sec}秒")
    print(f"矩阵大小: {matrix_size}x{matrix_size}\n")

    # 创建大型随机矩阵
    matrix = torch.randn(matrix_size, matrix_size, device=device)

    # 预热GPU
    print("预热GPU...")
    for _ in range(3):
        matrix @ matrix.T

    # 主测试循环
    print("开始压力测试...")
    start_time = time.time()
    operations = 0

    try:
        while time.time() - start_time < duration_sec:
            # 执行矩阵乘法
            result = matrix @ matrix.T

            # 添加非线性操作增加压力
            result = torch.sigmoid(result) * torch.tanh(result)

            operations += 1

            # 每5秒报告一次
            if int(time.time() - start_time) % 5 == 0:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] "
                      f"运行时间: {int(time.time() - start_time)}秒 | "
                      f"操作次数: {operations}")

    except KeyboardInterrupt:
        print("\n测试中断")

    # 清理显存
    del matrix, result
    torch.cuda.empty_cache()

    # 结果报告
    total_time = time.time() - start_time
    print("\n=== 测试结果 ===")
    print(f"总运行时间: {total_time:.2f}秒")
    print(f"完成操作次数: {operations}")
    print(f"平均操作频率: {operations/total_time:.2f} 操作/秒")
    print(f"峰值显存使用: {torch.cuda.max_memory_allocated(device=device)/1e9:.2f} GB")
    print(f"当前显存使用: {torch.cuda.memory_allocated(device=device)/1e9:.2f} GB")
    print("测试完成！建议同时使用nvidia-smi监控GPU利用率")

if __name__ == "__main__":
    # 配置测试参数（可根据需要调整）
    gpu_stress_test(
        duration_sec=60,    # 测试时长(秒)
        matrix_size=10000   # 矩阵大小(NxN)
    )