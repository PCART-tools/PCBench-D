import torch.nn as nn
from transformers import Trainer, TrainingArguments
import inspect

class DummyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(10, 2)

    def forward(self, input_ids=None, attention_mask=None, labels=None):
        return self.linear(input_ids.float())

def main():
    model = DummyModel()
    training_args = TrainingArguments(
        output_dir="./results",
        per_device_train_batch_size=8,
    )
    trainer = Trainer(
        model=model,
        args=training_args
    )
    result = trainer.is_local_master()
    print("is_local_master result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(Trainer.is_local_master))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
