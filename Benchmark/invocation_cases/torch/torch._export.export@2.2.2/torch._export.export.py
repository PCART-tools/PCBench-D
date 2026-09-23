import torch
import inspect

def main():
    # Create a simple model
    class SimpleModel(torch.nn.Module):
        def forward(self, x):
            return x * 2

    model = SimpleModel()
    example_input = torch.tensor([1.0, 2.0, 3.0])

    # Export the model
    exported_model = torch._export.export(model, (example_input,))
    print("Exported model:", exported_model)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(torch._export.export))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()