import torch
from transformers import TransfoXLLMHeadModel, TransfoXLConfig
import inspect
import transformers.modeling_transfo_xl

def main():
    config = TransfoXLConfig()
    model = TransfoXLLMHeadModel(config)
    model.reset_length(512, 0, 512)  # tgt_len=512, ext_len=0, mem_len=512
    print("reset_length called successfully.")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(model.reset_length))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
