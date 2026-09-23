    @classmethod
    def _from_pretrained(cls, pretrained_model_name_or_path, *init_inputs, **kwargs):
        cache_dir = kwargs.pop("cache_dir", None)
        force_download = kwargs.pop("force_download", False)
        resume_download = kwargs.pop("resume_download", False)
        proxies = kwargs.pop("proxies", None)
        local_files_only = kwargs.pop("local_files_only", False)

        s3_models = list(cls.max_model_input_sizes.keys())
        vocab_files = {}
        init_configuration = {}
        if pretrained_model_name_or_path in s3_models:
            # Get the vocabulary from AWS S3 bucket
            for file_id, map_list in cls.pretrained_vocab_files_map.items():
                vocab_files[file_id] = map_list[pretrained_model_name_or_path]
            if (
                cls.pretrained_init_configuration
                and pretrained_model_name_or_path in cls.pretrained_init_configuration
            ):
                init_configuration = cls.pretrained_init_configuration[pretrained_model_name_or_path].copy()
        else:
            # Get the vocabulary from local files
            logger.info(
                "Model name '{}' not found in model shortcut name list ({}). "
                "Assuming '{}' is a path, a model identifier, or url to a directory containing tokenizer files.".format(
                    pretrained_model_name_or_path, ", ".join(s3_models), pretrained_model_name_or_path
                )
            )

            if os.path.isfile(pretrained_model_name_or_path) or is_remote_url(pretrained_model_name_or_path):
                if len(cls.vocab_files_names) > 1:
                    raise ValueError(
                        "Calling {}.from_pretrained() with the path to a single file or url is not supported."
                        "Use a model identifier or the path to a directory instead.".format(cls.__name__)
                    )
                logger.warning(
                    "Calling {}.from_pretrained() with the path to a single file or url is deprecated".format(
                        cls.__name__
                    )
                )
                file_id = list(cls.vocab_files_names.keys())[0]
                vocab_files[file_id] = pretrained_model_name_or_path
            else:
                # At this point pretrained_model_name_or_path is either a directory or a model identifier name
                additional_files_names = {
                    "added_tokens_file": ADDED_TOKENS_FILE,
                    "special_tokens_map_file": SPECIAL_TOKENS_MAP_FILE,
                    "tokenizer_config_file": TOKENIZER_CONFIG_FILE,
                    "full_tokenizer_file": FULL_TOKENIZER_FILE,
                }
                # Look for the tokenizer files
                for file_id, file_name in {**cls.vocab_files_names, **additional_files_names}.items():
                    if os.path.isdir(pretrained_model_name_or_path):
                        full_file_name = os.path.join(pretrained_model_name_or_path, file_name)
                        if not os.path.exists(full_file_name):
                            logger.info("Didn't find file {}. We won't load it.".format(full_file_name))
                            full_file_name = None
                    else:
                        full_file_name = hf_bucket_url(
                            pretrained_model_name_or_path, filename=file_name, use_cdn=False, mirror=None
                        )

                    vocab_files[file_id] = full_file_name

        # Get files from url, cache, or disk depending on the case
        try:
            resolved_vocab_files = {}
            for file_id, file_path in vocab_files.items():
                if file_path is None:
                    resolved_vocab_files[file_id] = None
                else:
                    resolved_vocab_files[file_id] = cached_path(
                        file_path,
                        cache_dir=cache_dir,
                        force_download=force_download,
                        proxies=proxies,
                        resume_download=resume_download,
                        local_files_only=local_files_only,
                    )
        except EnvironmentError:
            if pretrained_model_name_or_path in s3_models:
                msg = "Couldn't reach server at '{}' to download vocabulary files."
            else:
                msg = (
                    "Model name '{}' was not found in tokenizers model name list ({}). "
                    "We assumed '{}' was a path or url to a directory containing vocabulary files "
                    "named {}, but couldn't find such vocabulary files at this path or url.".format(
                        pretrained_model_name_or_path,
                        ", ".join(s3_models),
                        pretrained_model_name_or_path,
                        list(cls.vocab_files_names.values()),
                    )
                )

            raise EnvironmentError(msg)

        if all(full_file_name is None for full_file_name in resolved_vocab_files.values()):
            raise EnvironmentError(
                "Model name '{}' was not found in tokenizers model name list ({}). "
                "We assumed '{}' was a path, a model identifier, or url to a directory containing vocabulary files "
                "named {} but couldn't find such vocabulary files at this path or url.".format(
                    pretrained_model_name_or_path,
                    ", ".join(s3_models),
                    pretrained_model_name_or_path,
                    list(cls.vocab_files_names.values()),
                )
            )

        for file_id, file_path in vocab_files.items():
            if file_path == resolved_vocab_files[file_id]:
                logger.info("loading file {}".format(file_path))
            else:
                logger.info("loading file {} from cache at {}".format(file_path, resolved_vocab_files[file_id]))

        # Prepare tokenizer initialization kwargs
        # Did we saved some inputs and kwargs to reload ?
        tokenizer_config_file = resolved_vocab_files.pop("tokenizer_config_file", None)
        if tokenizer_config_file is not None:
            with open(tokenizer_config_file, encoding="utf-8") as tokenizer_config_handle:
                init_kwargs = json.load(tokenizer_config_handle)
            saved_init_inputs = init_kwargs.pop("init_inputs", ())
            if not init_inputs:
                init_inputs = saved_init_inputs
        else:
            init_kwargs = init_configuration

        # Update with newly provided kwargs
        init_kwargs.update(kwargs)

        # Set max length if needed
        if pretrained_model_name_or_path in cls.max_model_input_sizes:
            # if we're using a pretrained model, ensure the tokenizer
            # wont index sequences longer than the number of positional embeddings
            model_max_length = cls.max_model_input_sizes[pretrained_model_name_or_path]
            if model_max_length is not None and isinstance(model_max_length, (int, float)):
                init_kwargs["model_max_length"] = min(init_kwargs.get("model_max_length", int(1e30)), model_max_length)

        # Merge resolved_vocab_files arguments in init_kwargs.
        added_tokens_file = resolved_vocab_files.pop("added_tokens_file", None)
        for args_name, file_path in resolved_vocab_files.items():
            if args_name not in init_kwargs:
                init_kwargs[args_name] = file_path

        # Instantiate tokenizer.
        try:
            tokenizer = cls(*init_inputs, **init_kwargs)
        except OSError:
            raise OSError(
                "Unable to load vocabulary from file. "
                "Please check that the provided vocabulary is accessible and not corrupted."
            )

        # Save inputs and kwargs for saving and re-loading with ``save_pretrained``
        tokenizer.init_inputs = init_inputs
        tokenizer.init_kwargs = init_kwargs

        # If there is a complementary special token map, load it
        special_tokens_map_file = resolved_vocab_files.pop("special_tokens_map_file", None)
        if special_tokens_map_file is not None:
            with open(special_tokens_map_file, encoding="utf-8") as special_tokens_map_handle:
                special_tokens_map = json.load(special_tokens_map_handle)

            for key, value in special_tokens_map.items():
                if isinstance(value, dict):
                    value = AddedToken(**value)
                elif isinstance(value, list):
                    value = [AddedToken(**token) if isinstance(token, dict) else token for token in value]
                setattr(tokenizer, key, value)

        # Add supplementary tokens.
        special_tokens = tokenizer.all_special_tokens
        if added_tokens_file is not None:
            with open(added_tokens_file, encoding="utf-8") as added_tokens_handle:
                added_tok_encoder = json.load(added_tokens_handle)

            # Sort added tokens by index
            added_tok_encoder_sorted = list(sorted(added_tok_encoder.items(), key=lambda x: x[1]))

            for token, index in added_tok_encoder_sorted:
                assert index == len(tokenizer), (
                    f"Non-consecutive added token '{token}' found. "
                    f"Should have index {len(tokenizer)} but has index {index} in saved vocabulary."
                )
                tokenizer.add_tokens(token, special_tokens=bool(token in special_tokens))

        # Check all our special tokens are registered as "no split" token (we don't cut them) and are in the vocab
        added_tokens = tokenizer.sanitize_special_tokens()
        if added_tokens:
            logger.warning(
                "Special tokens have been added in the vocabulary, make sure the associated word embedding are fine-tuned or trained."
            )

        return tokenizer
