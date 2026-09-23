import inspect
import torch
import torch.nn as nn
from transformers import Trainer, TrainingArguments


class DummyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(10, 1)

    def forward(self, input_ids=None, labels=None):
        loss = self.linear(torch.randn(1, 10)).mean()
        return {"loss": loss}

def main():
    args = TrainingArguments(output_dir="./results", per_device_train_batch_size=1)
    model = DummyModel()
    trainer = Trainer(model=model, args=args)

    
    result = trainer._log({'loss': 0.5})
    print("log result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(trainer._log))
    except Exception as e:
        print(type(e).__name__)
    

if __name__ == "__main__":
    main()
