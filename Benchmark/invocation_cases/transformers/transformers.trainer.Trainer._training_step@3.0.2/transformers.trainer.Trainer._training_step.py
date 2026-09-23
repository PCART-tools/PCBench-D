import torch
from torch import nn
from torch.utils.data import Dataset
from transformers import Trainer, TrainingArguments
import inspect

# Dummy dataset
class DummyDataset(Dataset):
    def __getitem__(self, idx):
        return {
            "input_ids": torch.randint(0, 100, (16,)),
            "attention_mask": torch.ones(16),
            "labels": torch.tensor(1)
        }

    def __len__(self):
        return 1

# Dummy model that returns (loss, logits)
class DummyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(16, 2)
        self.loss_fn = nn.CrossEntropyLoss()

    def forward(self, input_ids=None, attention_mask=None, labels=None):
        logits = self.linear(input_ids.float())
        loss = self.loss_fn(logits, labels)
        return loss, logits  # transformers 3.0.2 expects tuple

def main():
    model = DummyModel()
    dataset = DummyDataset()

    training_args = TrainingArguments(output_dir="./results", num_train_epochs=1)
    trainer = Trainer(model=model, args=training_args, train_dataset=dataset)

    # Prepare inputs (add batch dimension)
    inputs = dataset[0]
    for k in inputs:
        inputs[k] = inputs[k].unsqueeze(0)

    # Create a dummy optimizer
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    # Call _training_step with optimizer
    result = trainer._training_step(model, inputs, optimizer)
    print("_training_step result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(trainer._training_step))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
