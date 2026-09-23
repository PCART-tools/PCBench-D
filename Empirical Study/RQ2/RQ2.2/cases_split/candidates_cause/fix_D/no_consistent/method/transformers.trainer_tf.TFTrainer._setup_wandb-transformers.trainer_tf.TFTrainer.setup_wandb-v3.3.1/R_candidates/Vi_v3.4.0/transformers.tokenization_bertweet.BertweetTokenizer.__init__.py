    def __init__(
        self,
        vocab_file,
        merges_file,
        normalization=False,
        bos_token="<s>",
        eos_token="</s>",
        sep_token="</s>",
        cls_token="<s>",
        unk_token="<unk>",
        pad_token="<pad>",
        mask_token="<mask>",
        **kwargs
    ):
        super().__init__(
            bos_token=bos_token,
            eos_token=eos_token,
            unk_token=unk_token,
            sep_token=sep_token,
            cls_token=cls_token,
            pad_token=pad_token,
            mask_token=mask_token,
            **kwargs,
        )

        try:
            from emoji import demojize

            self.demojizer = demojize
        except ImportError:
            logger.warning(
                "emoji is not installed, thus not converting emoticons or emojis into text. Please install emoji: pip3 install emoji"
            )
            self.demojizer = None

        self.vocab_file = vocab_file
        self.merges_file = merges_file

        self.encoder = {}
        self.encoder[self.bos_token] = 0
        self.encoder[self.pad_token] = 1
        self.encoder[self.eos_token] = 2
        self.encoder[self.unk_token] = 3

        self.add_from_file(vocab_file)

        self.decoder = {v: k for k, v in self.encoder.items()}

        with open(merges_file, encoding="utf-8") as merges_handle:
            merges = merges_handle.read().split("\n")[:-1]
        merges = [tuple(merge.split()[:-1]) for merge in merges]
        self.bpe_ranks = dict(zip(merges, range(len(merges))))
        self.cache = {}

        self.normalization = normalization
        self.tweetPreprocessor = TweetTokenizer()

        self.special_puncts = {"’": "'", "…": "..."}
