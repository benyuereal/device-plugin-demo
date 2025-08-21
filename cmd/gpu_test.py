import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

def main():
    # 设备检测
    print("="*50)
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")

    if torch.cuda.is_available():
        # 验证device plugin资源
        print(f"Detected {torch.cuda.device_count()} GPU device(s):")
        for i in range(torch.cuda.device_count()):
            print(f"Device {i}: {torch.cuda.get_device_name(i)}")
            print(f"  Memory: {torch.cuda.get_device_properties(i).total_memory/1024**2:.2f} MB")
    else:
        print("!! ERROR: No CUDA devices detected !!")
        return

    print("="*50)
    print("Testing model loading and inference...")

    try:
        # 模型路径
        model_path = "/model"

        # 加载模型
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        print(f"Model successfully loaded on device: {model.device}")

        # 测试推理
        prompt = "Explain the purpose of a GPU device plugin in Kubernetes"
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

        outputs = model.generate(
            **inputs,
            max_new_tokens=50,
            do_sample=True
        )

        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        print("\nModel response:")
        print("-"*50)
        print(response)
        print("-"*50)
        print("✅ Test successful!")

    except Exception as e:
        print(f"!! TEST FAILED: {str(e)}")
        raise

if __name__ == "__main__":
    main()