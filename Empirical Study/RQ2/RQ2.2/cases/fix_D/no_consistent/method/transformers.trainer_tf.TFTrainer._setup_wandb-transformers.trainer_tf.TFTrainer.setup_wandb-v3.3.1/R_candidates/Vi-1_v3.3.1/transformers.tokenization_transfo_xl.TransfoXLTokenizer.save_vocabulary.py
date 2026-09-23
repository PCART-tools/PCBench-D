    def save_vocabulary(self, vocab_path):
        """
        Save the vocabulary and special tokens file to a directory.

        Args:
            vocab_path (:obj:`str`):
                The directory in which to save the vocabulary.

        Returns:
            :obj:`Tuple(str)`: Paths to the files saved.
        """

        logger.warning(
            "Please note you will not be able to load the save vocabulary in"
            " Rust-based TransfoXLTokenizerFast as they don't share the same structure."
        )

        if os.path.isdir(vocab_path):
            vocab_file = os.path.join(vocab_path, VOCAB_FILES_NAMES["pretrained_vocab_file"])
        else:
            vocab_file = vocab_path
        torch.save(self.__dict__, vocab_file)
        return (vocab_file,)
