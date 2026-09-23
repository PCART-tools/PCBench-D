    @classmethod
    @replace_list_option_in_docstrings(TF_MODEL_FOR_SEQ_TO_SEQ_CAUSAL_LM_MAPPING, use_model_types=False)
    def from_config(cls, config):
        r"""
        Instantiates one of the model classes of the library---with a sequence-to-sequence language modeling
        head---from a configuration.

        Note:
            Loading a model from its configuration file does **not** load the model weights. It only affects the
            model's configuration. Use :meth:`~transformers.TFAutoModelForSeq2SeqLM.from_pretrained` to load the model
            weights.

        Args:
            config (:class:`~transformers.PretrainedConfig`):
                The model class to instantiate is selected based on the configuration class:

                List options

        Examples::

            >>> from transformers import AutoConfig, TFAutoModelForSeq2SeqLM
            >>> # Download configuration from S3 and cache.
            >>> config = AutoConfig.from_pretrained('t5')
            >>> model = TFAutoModelForSeq2SeqLM.from_config(config)
        """
        if type(config) in TF_MODEL_FOR_SEQ_TO_SEQ_CAUSAL_LM_MAPPING.keys():
            return TF_MODEL_FOR_SEQ_TO_SEQ_CAUSAL_LM_MAPPING[type(config)](config)
        raise ValueError(
            "Unrecognized configuration class {} for this kind of TFAutoModel: {}.\n"
            "Model type should be one of {}.".format(
                config.__class__,
                cls.__name__,
                ", ".join(c.__name__ for c in TF_MODEL_FOR_SEQ_TO_SEQ_CAUSAL_LM_MAPPING.keys()),
            )
        )
