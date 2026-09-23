from transformers import Trainer, TrainingArguments
import inspect
import torch.nn as nn

class DummyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(10, 10)

    def forward(self, x):
        return self.linear(x)

def main():
    model = DummyModel()
    training_args = TrainingArguments(output_dir='./results')
    trainer = Trainer(model=model, args=training_args)
    result = trainer.is_world_master()
    print("is_world_master result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(trainer.is_world_master))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()