    @classmethod
    @replace_list_option_in_docstrings(MODEL_FOR_SEQUENCE_CLASSIFICATION_MAPPING, use_model_types=False)
    def from_config(cls, config):
        r"""
        Instantiates one of the model classes of the library---with a sequence classification head---from a
        configuration.

        Note:
            Loading a model from its configuration file does **not** load the model weights. It only affects the
            model's configuration. Use :meth:`~transformers.AutoModelForSequenceClassification.from_pretrained` to load
            the model weights.

        Args:
            config (:class:`~transformers.PretrainedConfig`):
                The model class to instantiate is selected based on the configuration class:

                List options

        Examples::

            >>> from transformers import AutoConfig, AutoModelForSequenceClassification
            >>> # Download configuration from S3 and cache.
            >>> config = AutoConfig.from_pretrained('bert-base-uncased')
            >>> model = AutoModelForSequenceClassification.from_config(config)
        """
        if type(config) in MODEL_FOR_SEQUENCE_CLASSIFICATION_MAPPING.keys():
            return MODEL_FOR_SEQUENCE_CLASSIFICATION_MAPPING[type(config)](config)
        raise ValueError(
            "Unrecognized configuration class {} for this kind of AutoModel: {}.\n"
            "Model type should be one of {}.".format(
                config.__class__,
                cls.__name__,
                ", ".join(c.__name__ for c in MODEL_FOR_SEQUENCE_CLASSIFICATION_MAPPING.keys()),
            )
        )
