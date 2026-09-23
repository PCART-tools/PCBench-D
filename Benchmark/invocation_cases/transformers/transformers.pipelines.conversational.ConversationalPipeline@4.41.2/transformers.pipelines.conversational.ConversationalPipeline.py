import inspect
from transformers import (
    AutoConfig,
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    ConversationalPipeline
)

def main():
    model_name = "facebook/blenderbot-400M-distill"
    config = AutoConfig.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_config(config)
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        use_fast=True
    )

    chatbot = ConversationalPipeline(
        model=model,
        tokenizer=tokenizer,
        framework="pt",
        device=-1,
        task="conversational"
    )

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(ConversationalPipeline))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()