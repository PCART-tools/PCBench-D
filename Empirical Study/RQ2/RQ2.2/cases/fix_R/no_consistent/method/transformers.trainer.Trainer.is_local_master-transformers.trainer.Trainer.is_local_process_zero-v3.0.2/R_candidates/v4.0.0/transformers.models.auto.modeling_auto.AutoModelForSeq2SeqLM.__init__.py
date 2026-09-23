    def __init__(self):
        raise EnvironmentError(
            "AutoModelForSeq2SeqLM is designed to be instantiated "
            "using the `AutoModelForSeq2SeqLM.from_pretrained(pretrained_model_name_or_path)` or "
            "`AutoModelForSeq2SeqLM.from_config(config)` methods."
        )
