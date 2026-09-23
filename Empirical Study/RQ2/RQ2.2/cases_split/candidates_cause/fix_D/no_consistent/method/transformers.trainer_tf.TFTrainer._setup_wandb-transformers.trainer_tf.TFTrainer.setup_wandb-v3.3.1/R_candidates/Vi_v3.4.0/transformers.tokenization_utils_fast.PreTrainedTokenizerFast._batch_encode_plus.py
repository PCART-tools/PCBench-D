    def _batch_encode_plus(
        self,
        batch_text_or_text_pairs: Union[
            List[TextInput], List[TextInputPair], List[PreTokenizedInput], List[PreTokenizedInputPair]
        ],
        add_special_tokens: bool = True,
        padding_strategy: PaddingStrategy = PaddingStrategy.DO_NOT_PAD,
        truncation_strategy: TruncationStrategy = TruncationStrategy.DO_NOT_TRUNCATE,
        max_length: Optional[int] = None,
        stride: int = 0,
        is_split_into_words: bool = False,
        pad_to_multiple_of: Optional[int] = None,
        return_tensors: Optional[str] = None,
        return_token_type_ids: Optional[bool] = None,
        return_attention_mask: Optional[bool] = None,
        return_overflowing_tokens: bool = False,
        return_special_tokens_mask: bool = False,
        return_offsets_mapping: bool = False,
        return_length: bool = False,
        verbose: bool = True,
        **kwargs
    ) -> BatchEncoding:

        if not isinstance(batch_text_or_text_pairs, list):
            raise TypeError(
                "batch_text_or_text_pairs has to be a list (got {})".format(type(batch_text_or_text_pairs))
            )

        if "is_pretokenized" in kwargs:
            warnings.warn(
                "`is_pretokenized` is deprecated and will be removed in a future version, use `is_split_into_words` instead.",
                FutureWarning,
            )
            is_split_into_words = kwargs.pop("is_pretokenized")

        if kwargs:
            raise ValueError(f"Keyword arguments {kwargs} not recognized.")

        # Set the truncation and padding strategy and restore the initial configuration
        self.set_truncation_and_padding(
            padding_strategy=padding_strategy,
            truncation_strategy=truncation_strategy,
            max_length=max_length,
            stride=stride,
            pad_to_multiple_of=pad_to_multiple_of,
        )

        # Avoid thread overhead if only one example.
        if len(batch_text_or_text_pairs) == 1:
            if isinstance(batch_text_or_text_pairs[0], tuple):
                # We got a Tuple with a pair of sequences
                encodings = self._tokenizer.encode(
                    *batch_text_or_text_pairs[0],
                    add_special_tokens=add_special_tokens,
                    is_pretokenized=is_split_into_words,
                )
            else:
                # We got a single sequence
                encodings = self._tokenizer.encode(
                    batch_text_or_text_pairs[0],
                    add_special_tokens=add_special_tokens,
                    is_pretokenized=is_split_into_words,
                )
            encodings = [encodings]
        else:
            encodings = self._tokenizer.encode_batch(
                batch_text_or_text_pairs,
                add_special_tokens=add_special_tokens,
                is_pretokenized=is_split_into_words,
            )

        # Convert encoding to dict
        # `Tokens` has type: List[Dict[str, List[List[int]]]] or List[Dict[str, 2D-Tensor]]
        # with nested dimensions corresponding to batch, overflows, sequence length
        tokens = [
            self._convert_encoding(
                encoding=encoding,
                return_token_type_ids=return_token_type_ids,
                return_attention_mask=return_attention_mask,
                return_overflowing_tokens=return_overflowing_tokens,
                return_special_tokens_mask=return_special_tokens_mask,
                return_offsets_mapping=return_offsets_mapping,
                return_length=return_length,
                verbose=verbose,
            )
            for encoding in encodings
        ]

        # Convert the output to have dict[list] from list[dict]
        sanitized = {}
        for key in tokens[0].keys():
            # To List[List[List[int]]] of shape (batch, overflows, sequence length)
            stack = [e for item in tokens for e in item[key]]
            sanitized[key] = stack

        # If returning overflowing tokens, we need to return a mapping
        # from the batch idx to the original sample
        if return_overflowing_tokens:
            overflow_to_sample_mapping = []
            for i, enc in enumerate(tokens):
                overflow_to_sample_mapping += [i] * len(enc["input_ids"])
            sanitized["overflow_to_sample_mapping"] = overflow_to_sample_mapping

        return BatchEncoding(sanitized, encodings, tensor_type=return_tensors)
