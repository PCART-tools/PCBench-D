    def __init__(self):
        raise EnvironmentError(
            "AutoModelForMaskedLM is designed to be instantiated "
            "using the `AutoModelForMaskedLM.from_pretrained(pretrained_model_name_or_path)` or "
            "`AutoModelForMaskedLM.from_config(config)` methods."
        )
