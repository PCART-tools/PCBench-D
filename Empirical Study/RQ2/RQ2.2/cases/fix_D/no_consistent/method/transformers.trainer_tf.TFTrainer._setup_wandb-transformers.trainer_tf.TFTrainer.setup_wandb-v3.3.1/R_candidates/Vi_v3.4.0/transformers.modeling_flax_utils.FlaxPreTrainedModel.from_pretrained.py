    @classmethod
    def from_pretrained(cls, pretrained_model_name_or_path, *model_args, **kwargs):
        r"""
        Instantiate a pretrained Flax model from a pre-trained model configuration.
        """
        config = kwargs.pop("config", None)
        # state_dict = kwargs.pop("state_dict", None)
        cache_dir = kwargs.pop("cache_dir", None)
        # from_tf = kwargs.pop("from_tf", False)
        force_download = kwargs.pop("force_download", False)
        resume_download = kwargs.pop("resume_download", False)
        proxies = kwargs.pop("proxies", None)
        # output_loading_info = kwargs.pop("output_loading_info", False)
        local_files_only = kwargs.pop("local_files_only", False)
        use_cdn = kwargs.pop("use_cdn", True)

        # Load config if we don't provide a configuration
        if not isinstance(config, PretrainedConfig):
            config_path = config if config is not None else pretrained_model_name_or_path
            config, model_kwargs = cls.config_class.from_pretrained(
                config_path,
                *model_args,
                cache_dir=cache_dir,
                return_unused_kwargs=True,
                force_download=force_download,
                resume_download=resume_download,
                proxies=proxies,
                local_files_only=local_files_only,
                **kwargs,
            )
        else:
            model_kwargs = kwargs

        # Load model
        if pretrained_model_name_or_path is not None:
            if os.path.isfile(pretrained_model_name_or_path) or is_remote_url(pretrained_model_name_or_path):
                archive_file = pretrained_model_name_or_path
            else:
                archive_file = hf_bucket_url(pretrained_model_name_or_path, filename=WEIGHTS_NAME, use_cdn=use_cdn)

            # redirect to the cache, if necessary
            try:
                resolved_archive_file = cached_path(
                    archive_file,
                    cache_dir=cache_dir,
                    force_download=force_download,
                    proxies=proxies,
                    resume_download=resume_download,
                    local_files_only=local_files_only,
                )
            except EnvironmentError:
                if pretrained_model_name_or_path in cls.pretrained_model_archive_map:
                    msg = f"Couldn't reach server at '{archive_file}' to download pretrained weights."
                else:
                    msg = (
                        f"Model name '{pretrained_model_name_or_path}' "
                        f"was not found in model name list ({', '.join(cls.pretrained_model_archive_map.keys())}). "
                        f"We assumed '{archive_file}' was a path or url to model weight files but "
                        "couldn't find any such file at this path or url."
                    )
                raise EnvironmentError(msg)

            if resolved_archive_file == archive_file:
                logger.info(f"loading weights file {archive_file}")
            else:
                logger.info(f"loading weights file {archive_file} from cache at {resolved_archive_file}")
        else:
            resolved_archive_file = None

        # Instantiate model.
        with open(resolved_archive_file, "rb") as state_f:
            try:
                from flax.serialization import from_bytes

                state = from_bytes(cls.model_class, state_f)
            except TypeError:
                try:
                    import torch

                    state = torch.load(state_f)
                    state = {k: v.numpy() for k, v in state.items()}
                    state = cls.convert_from_pytorch(state, config)
                    state = unflatten_dict({tuple(k.split(".")[1:]): v for k, v in state.items()})
                except UnpicklingError:
                    raise EnvironmentError(
                        f"Unable to convert model {archive_file} to Flax deserializable object. "
                        "Supported format are PyTorch archive or Flax msgpack"
                    )

        return cls(config, state, *model_args, **model_kwargs)
