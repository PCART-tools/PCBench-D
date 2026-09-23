import inspect
from transformers import TFTransfoXLLMHeadModel

def main():
    model = TFTransfoXLLMHeadModel.from_pretrained(
        "transfo-xl-wt103",
        from_pt=True
    )

    tgt_len = 128
    ext_len = 64
    mem_len = 512
    model.reset_length(tgt_len, ext_len, mem_len)
    print("reset_length called successfully.")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(model.reset_length))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()