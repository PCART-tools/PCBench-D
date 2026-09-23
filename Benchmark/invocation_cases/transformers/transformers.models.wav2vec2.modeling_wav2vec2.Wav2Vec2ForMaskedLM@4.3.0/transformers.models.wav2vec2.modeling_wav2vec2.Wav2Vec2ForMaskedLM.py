import torch
from transformers.models.wav2vec2 import Wav2Vec2ForMaskedLM, Wav2Vec2Config
import inspect

def main():
    config = Wav2Vec2Config(
        vocab_size=32,
        hidden_size=64,
        num_hidden_layers=2,
        num_attention_heads=2,
        intermediate_size=256,
    )
    model = Wav2Vec2ForMaskedLM(config)

    input_values = torch.randn(1, 16000)

    with torch.no_grad():
        logits = model(input_values).logits

    print("Logits shape:", logits.shape)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(Wav2Vec2ForMaskedLM))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
