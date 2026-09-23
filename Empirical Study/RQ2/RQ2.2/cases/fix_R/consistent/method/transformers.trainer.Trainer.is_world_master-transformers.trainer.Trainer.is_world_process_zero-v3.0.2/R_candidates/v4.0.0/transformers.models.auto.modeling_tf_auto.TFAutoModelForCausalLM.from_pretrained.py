    @classmethod
    @replace_list_option_in_docstrings(TF_MODEL_FOR_CAUSAL_LM_MAPPING)
    @add_start_docstrings(
        "Instantiate one of the model classes of the library---with a causal language modeling head---from a "
        "pretrained model.",
        TF_AUTO_MODEL_PRETRAINED_DOCSTRING,
    )
    def from_pretrained(cls, pretrained_model_name_or_path, *model_args, **kwargs):
        r"""
        Examples::

            >>> from transformers import AutoConfig, TFAutoModelForCausalLM

            >>> # Download model and configuration from huggingface.co and cache.
            >>> model = TFAutoModelForCausalLM.from_pretrained('gpt2')

            >>> # Update configuration during loading
            >>> model = TFAutoModelForCausalLM.from_pretrained('gpt2', output_attentions=True)
            >>> model.config.output_attentions
            True

            >>> # Loading from a PyTorch checkpoint file instead of a TensorFlow model (slower)
            >>> config = AutoConfig.from_json_file('./pt_model/gpt2_pt_model_config.json')
            >>> model = TFAutoModelForCausalLM.from_pretrained('./pt_model/gpt2_pytorch_model.bin', from_pt=True, config=config)
        """
        config = kwargs.pop("config", None)
        if not isinstance(config, PretrainedConfig):
            config, kwargs = AutoConfig.from_pretrained(
                pretrained_model_name_or_path, return_unused_kwargs=True, **kwargs
            )

        if type(config) in TF_MODEL_FOR_CAUSAL_LM_MAPPING.keys():
            return TF_MODEL_FOR_CAUSAL_LM_MAPPING[type(config)].from_pretrained(
                pretrained_model_name_or_path, *model_args, config=config, **kwargs
            )
        raise ValueError(
            "Unrecognized configuration class {} for this kind of TFAutoModel: {}.\n"
            "Model type should be one of {}.".format(
                config.__class__, cls.__name__, ", ".join(c.__name__ for c in TF_MODEL_FOR_CAUSAL_LM_MAPPING.keys())
            )
        )
