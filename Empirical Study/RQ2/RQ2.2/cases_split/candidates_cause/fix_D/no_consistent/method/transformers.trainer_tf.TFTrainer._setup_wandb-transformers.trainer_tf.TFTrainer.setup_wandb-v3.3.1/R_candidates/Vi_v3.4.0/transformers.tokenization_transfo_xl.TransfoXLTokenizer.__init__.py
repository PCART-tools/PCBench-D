    def __init__(
        self,
        special=None,
        min_freq=0,
        max_size=None,
        lower_case=False,
        delimiter=None,
        vocab_file=None,
        pretrained_vocab_file: str = None,
        never_split=None,
        unk_token="<unk>",
        eos_token="<eos>",
        additional_special_tokens=["<formula>"],
        language="en",
        **kwargs
    ):
        super().__init__(
            unk_token=unk_token, eos_token=eos_token, additional_special_tokens=additional_special_tokens, **kwargs
        )

        if never_split is None:
            never_split = self.all_special_tokens
        if special is None:
            special = []
        self.counter = Counter()
        self.special = special
        self.min_freq = min_freq
        self.max_size = max_size
        self.lower_case = lower_case
        self.delimiter = delimiter
        self.vocab_file = vocab_file
        self.never_split = never_split
        self.punctuation_symbols = '!"#$%&()*+,-./\\:;<=>?@[\\]^_`{|}~'
        self.punction_without_space_before_pattern = re.compile(r"[^\s][{}]".format(self.punctuation_symbols))
        self.punctuation_with_space_around_pattern = self._compile_space_around_punctuation_pattern()
        self.language = language
        self.moses_punct_normalizer = sm.MosesPunctNormalizer(language)
        self.moses_tokenizer = sm.MosesTokenizer(language)
        self.moses_detokenizer = sm.MosesDetokenizer(language)

        # This try... catch... is not beautiful but honestly this tokenizer was not made to be used
        # in a library like ours, at all.
        try:
            vocab_dict = None
            if pretrained_vocab_file is not None:
                # Priority on pickle files (support PyTorch and TF)
                with open(pretrained_vocab_file, "rb") as f:
                    vocab_dict = pickle.load(f)

                # Loading a torch-saved transfo-xl vocab dict with pickle results in an integer
                # Entering this if statement means that we tried to load a torch-saved file with pickle, and we failed.
                # We therefore load it with torch, if it's available.
                if type(vocab_dict) == int:
                    if not is_torch_available():
                        raise ImportError(
                            "Not trying to load dict with PyTorch as you need to install pytorch to load "
                            "from a PyTorch pretrained vocabulary, "
                            "or activate it with environment variables USE_TORCH=1 and USE_TF=0."
                        )
                    vocab_dict = torch.load(pretrained_vocab_file)

            if vocab_dict is not None:
                for key, value in vocab_dict.items():
                    if key not in self.__dict__:
                        self.__dict__[key] = value
            elif vocab_file is not None:
                self.build_vocab()

        except Exception as e:
            raise ValueError(
                "Unable to parse file {}. Unknown format. "
                "If you tried to load a model saved through TransfoXLTokenizerFast,"
                "please note they are not compatible.".format(pretrained_vocab_file)
            ) from e

        if vocab_file is not None:
            self.build_vocab()
