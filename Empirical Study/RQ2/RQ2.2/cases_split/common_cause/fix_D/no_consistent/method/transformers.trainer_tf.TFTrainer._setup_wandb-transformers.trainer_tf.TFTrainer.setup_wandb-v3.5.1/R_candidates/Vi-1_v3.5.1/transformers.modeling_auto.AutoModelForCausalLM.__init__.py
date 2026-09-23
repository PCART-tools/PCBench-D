    def __init__(self):
        raise EnvironmentError(
            "AutoModelForCausalLM is designed to be instantiated "
            "using the `AutoModelForCausalLM.from_pretrained(pretrained_model_name_or_path)` or "
            "`AutoModelForCausalLM.from_config(config)` methods."
        )
