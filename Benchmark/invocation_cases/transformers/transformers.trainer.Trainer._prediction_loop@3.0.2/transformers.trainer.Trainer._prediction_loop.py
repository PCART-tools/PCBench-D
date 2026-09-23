import inspect
import torch
import torch.nn as nn
from torch.utils.data import Dataset
from transformers import Trainer, TrainingArguments

# Dummy dataset
class DummyDataset(Dataset):
    def __len__(self):
        return 10

    def __getitem__(self, idx):
        return {
            "input_ids": torch.randint(0, 100, (32,)),
            "attention_mask": torch.ones(32),
            "labels": torch.tensor(1)
        }

# Dummy model
class DummyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.classifier = nn.Linear(32, 2)

    def forward(self, input_ids=None, attention_mask=None, labels=None):
        logits = self.classifier(input_ids.float())
        loss_fn = nn.CrossEntropyLoss()
        loss = loss_fn(logits, labels)
        return loss, logits, labels  

def main():
    dataset = DummyDataset()
    model = DummyModel()

    training_args = TrainingArguments(
        output_dir="./results",
        per_device_train_batch_size=2,
        num_train_epochs=1
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset
    )

    dataloader = trainer.get_test_dataloader(dataset)
    result = trainer._prediction_loop(dataloader, description="Prediction")
    print("Prediction result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(trainer._prediction_loop))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
