    def __init__(
        self,
        special=None,
        min_freq=0,
        max_size=None,
        lower_case=False,
        delimiter=None,
        vocab_file=None,
        pretrained_vocab_file=None,
        never_split=None,
        unk_token="<unk>",
        eos_token="<eos>",
        additional_special_tokens=["<formula>"],
        add_eos=False,
        add_double_eos=False,
        normalization=None,
        **kwargs
    ):

        super().__init__(
            _TransfoXLDelimiterLookupTokenizer(
                vocab_file=vocab_file or pretrained_vocab_file,
                delimiter=delimiter,
                lowercase=lower_case,
                unk_token=unk_token,
                eos_token=eos_token,
                add_eos=add_eos,
                add_double_eos=add_double_eos,
                normalization=normalization,
            ),
            unk_token=unk_token,
            eos_token=eos_token,
            additional_special_tokens=additional_special_tokens,
            **kwargs,
        )

        warnings.warn(
            "The class `TransfoXLTokenizerFast` is deprecated and will be removed in a future version. Please use `TransfoXLTokenizer` with it's enhanced tokenization instead.",
            FutureWarning,
        )
