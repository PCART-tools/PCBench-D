import inspect
import tensorflow as tf
from transformers import TFTrainer, TFTrainingArguments
from transformers.modeling_tf_utils import TFPreTrainedModel
from transformers.configuration_utils import PretrainedConfig

class DummyConfig(PretrainedConfig):
    pass


class DummyTFModel(TFPreTrainedModel):
    def __init__(self, config):
        super().__init__(config)
        self.dense = tf.keras.layers.Dense(2)

    def call(self, features, labels=None, training=False):
        x = tf.cast(features["input_ids"], tf.float32)
        logits = self.dense(x)
        loss = tf.reduce_mean(logits)
        return loss, logits


def main():
    features = {
        "input_ids": tf.ones((1, 4), dtype=tf.int32)
    }
    labels = tf.zeros((1,), dtype=tf.int32)
    dataset = tf.data.Dataset.from_tensor_slices((features, labels)).batch(1)
    args = TFTrainingArguments(output_dir="/tmp")
    trainer = TFTrainer(model=DummyTFModel(DummyConfig()), args=args)
    loss, logits = trainer._run_model(
        features=features,
        labels=labels,
        training=True
    )
    
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(trainer._run_model))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
