    @classmethod
    @replace_list_option_in_docstrings(TF_MODEL_MAPPING, use_model_types=False)
    def from_config(cls, config):
        r"""
        Instantiates one of the base model classes of the library from a configuration.

        Note:
            Loading a model from its configuration file does **not** load the model weights. It only affects the
            model's configuration. Use :meth:`~transformers.TFAutoModel.from_pretrained` to load the model weights.

        Args:
            config (:class:`~transformers.PretrainedConfig`):
                The model class to instantiate is selected based on the configuration class:

                List options

        Examples::

            >>> from transformers import AutoConfig, TFAutoModel
            >>> # Download configuration from S3 and cache.
            >>> config = TFAutoConfig.from_pretrained('bert-base-uncased')
            >>> model = TFAutoModel.from_config(config)
        """
        if type(config) in TF_MODEL_MAPPING.keys():
            return TF_MODEL_MAPPING[type(config)](config)
        raise ValueError(
            "Unrecognized configuration class {} for this kind of TFAutoModel: {}.\n"
            "Model type should be one of {}.".format(
                config.__class__, cls.__name__, ", ".join(c.__name__ for c in TF_MODEL_MAPPING.keys())
            )
        )
