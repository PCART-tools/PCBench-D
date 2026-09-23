    def save_pretrained(self, save_directory: str) -> Tuple[str]:
        """
        Save the tokenizer vocabulary files together with:

            - added tokens,
            - special tokens to class attributes mapping,
            - tokenizer instantiation positional and keywords inputs (e.g. do_lower_case for Bert).

        This method make sure the full tokenizer can then be re-loaded using the
        :meth:`~transformers.tokenization_utils_base.PreTrainedTokenizerBase.from_pretrained` class method.

        .. Warning::
           This won't save modifications you may have applied to the tokenizer after the instantiation (for instance,
           modifying :obj:`tokenizer.do_lower_case` after creation).

        Args:
            save_directory (:obj:`str`): The path to adirectory where the tokenizer will be saved.

        Returns:
            A tuple of :obj:`str`: The files saved.
        """
        if os.path.isfile(save_directory):
            logger.error("Provided path ({}) should be a directory, not a file".format(save_directory))
            return
        os.makedirs(save_directory, exist_ok=True)

        special_tokens_map_file = os.path.join(save_directory, SPECIAL_TOKENS_MAP_FILE)
        added_tokens_file = os.path.join(save_directory, ADDED_TOKENS_FILE)
        tokenizer_config_file = os.path.join(save_directory, TOKENIZER_CONFIG_FILE)

        tokenizer_config = copy.deepcopy(self.init_kwargs)
        if len(self.init_inputs) > 0:
            tokenizer_config["init_inputs"] = copy.deepcopy(self.init_inputs)
        for file_id in self.vocab_files_names.keys():
            tokenizer_config.pop(file_id, None)

        with open(tokenizer_config_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(tokenizer_config, ensure_ascii=False))

        with open(special_tokens_map_file, "w", encoding="utf-8") as f:
            write_dict = {}
            for key, value in self.special_tokens_map_extended.items():
                if isinstance(value, AddedToken):
                    write_dict[key] = value.__getstate__()
                elif isinstance(value, list):
                    write_dict[key] = [
                        token.__getstate__() if isinstance(token, AddedToken) else token for token in value
                    ]
                else:
                    write_dict[key] = value
            f.write(json.dumps(write_dict, ensure_ascii=False))

        added_vocab = self.get_added_vocab()
        if added_vocab:
            with open(added_tokens_file, "w", encoding="utf-8") as f:
                out_str = json.dumps(added_vocab, ensure_ascii=False)
                f.write(out_str)

        vocab_files = self.save_vocabulary(save_directory)

        return vocab_files + (special_tokens_map_file, added_tokens_file)
