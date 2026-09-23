    @classmethod
    @replace_list_option_in_docstrings(TF_MODEL_WITH_LM_HEAD_MAPPING)
    @add_start_docstrings(
        "Instantiate one of the model classes of the library---with a language modeling head---from a pretrained ",
        "model.",
        TF_AUTO_MODEL_PRETRAINED_DOCSTRING,
    )
    def from_pretrained(cls, pretrained_model_name_or_path, *model_args, **kwargs):
        r"""
        Examples::

            >>> from transformers import AutoConfig, TFAutoModelWithLMHead

            >>> # Download model and configuration from S3 and cache.
            >>> model = TFAutoModelWithLMHead.from_pretrained('bert-base-uncased')

            >>> # Update configuration during loading
            >>> model = TFAutoModelWithLMHead.from_pretrained('bert-base-uncased', output_attentions=True)
            >>> model.config.output_attentions
            True

            >>> # Loading from a PyTorch checkpoint file instead of a TensorFlow model (slower)
            >>> config = AutoConfig.from_json_file('./pt_model/bert_pt_model_config.json')
            >>> model = TFAutoModelWithLMHead.from_pretrained('./pt_model/bert_pytorch_model.bin', from_pt=True, config=config)
        """
        warnings.warn(
            "The class `TFAutoModelWithLMHead` is deprecated and will be removed in a future version. Please use "
            "`TFAutoModelForCausalLM` for causal language models, `TFAutoModelForMaskedLM` for masked language models "
            "and `TFAutoModelForSeq2SeqLM` for encoder-decoder models.",
            FutureWarning,
        )
        config = kwargs.pop("config", None)

        if not isinstance(config, PretrainedConfig):
            config, kwargs = AutoConfig.from_pretrained(
                pretrained_model_name_or_path, return_unused_kwargs=True, **kwargs
            )

        if type(config) in TF_MODEL_WITH_LM_HEAD_MAPPING.keys():
            return TF_MODEL_WITH_LM_HEAD_MAPPING[type(config)].from_pretrained(
                pretrained_model_name_or_path, *model_args, config=config, **kwargs
            )
        raise ValueError(
            "Unrecognized configuration class {} for this kind of TFAutoModel: {}.\n"
            "Model type should be one of {}.".format(
                config.__class__, cls.__name__, ", ".join(c.__name__ for c in TF_MODEL_WITH_LM_HEAD_MAPPING.keys())
            )
        )
