    def save_vocabulary(self, save_directory) -> Tuple[str]:
        """
        Save the tokenizer vocabulary to a directory. This method does *NOT* save added tokens
        and special token mappings.

        .. warning::
            Please use :meth:`~transformers.PreTrainedTokenizer.save_pretrained` to save the full tokenizer state if
            you want to reload it using the :meth:`~transformers.PreTrainedTokenizer.from_pretrained` class method.

        Args:
            save_directory (:obj:`str`): The path to adirectory where the tokenizer will be saved.

        Returns:
            A tuple of :obj:`str`: The files saved.
        """
        raise NotImplementedError
