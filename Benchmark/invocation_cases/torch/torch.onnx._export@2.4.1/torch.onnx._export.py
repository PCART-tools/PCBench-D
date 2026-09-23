import torch
import torch.nn as nn
import torch.onnx
import inspect
import io

def main():
    class SimpleModel(nn.Module):
        def __init__(self):
            super(SimpleModel, self).__init__()
            self.fc = nn.Linear(10, 5)

        def forward(self, x):
            return self.fc(x)
    model = SimpleModel()
    dummy_input = torch.randn(1, 10)
    f = io.BytesIO()
    torch.onnx._export(model, dummy_input, f)
    print("Model exported to ONNX format.")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(torch.onnx._export))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()