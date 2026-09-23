    def __init__(
        self,
        vocab_file,
        delimiter,
        lowercase,
        unk_token,
        eos_token,
        add_eos=False,
        add_double_eos=False,
        normalization: Optional[str] = None,
    ):

        try:
            tokenizer = WordLevel(vocab_file, unk_token=unk_token)
            tokenizer = Tokenizer(tokenizer)
        except Exception:
            raise ValueError(
                "Unable to parse file {}. Unknown format. "
                "If you tried to load a model saved through TransfoXLTokenizer,"
                "please note they are not compatible.".format(vocab_file)
            )

        # Create the correct normalization path
        normalizer = []

        # Include unicode normalization
        if normalization:
            normalizer += [unicode_normalizer_from_str(normalization)]

        # Include case normalization
        if lowercase:
            normalizer += [Lowercase()]

        # Strip normalizer at the end
        normalizer += [Strip(left=True, right=True)]

        if len(normalizer) > 0:
            tokenizer.normalizer = Sequence(normalizer) if len(normalizer) > 1 else normalizer[0]

        # Setup the splitter
        tokenizer.pre_tokenizer = CharDelimiterSplit(delimiter) if delimiter else WhitespaceSplit()

        if add_double_eos:
            tokenizer.post_processor = BertProcessing(
                (eos_token, tokenizer.token_to_id(eos_token)), (eos_token, tokenizer.token_to_id(eos_token))
            )

        parameters = {
            "model": "TransfoXLModel",
            "add_eos": add_eos,
            "add_double_eos": add_double_eos,
            "unk_token": unk_token,
            "eos_token": eos_token,
            "delimiter": delimiter,
            "lowercase": lowercase,
        }

        super().__init__(tokenizer, parameters)
