    def __init__(
        self,
        vocab_file,
        do_lower_case=True,
        unk_token="[UNK]",
        sep_token="[SEP]",
        pad_token="[PAD]",
        cls_token="[CLS]",
        mask_token="[MASK]",
        clean_text=True,
        tokenize_chinese_chars=True,
        strip_accents=None,
        wordpieces_prefix="##",
        **kwargs
    ):
        super().__init__(
            BertWordPieceTokenizer(
                vocab_file=vocab_file,
                unk_token=unk_token,
                sep_token=sep_token,
                cls_token=cls_token,
                pad_token=pad_token,
                mask_token=mask_token,
                clean_text=clean_text,
                handle_chinese_chars=tokenize_chinese_chars,
                strip_accents=strip_accents,
                lowercase=do_lower_case,
                wordpieces_prefix=wordpieces_prefix,
            ),
            unk_token=unk_token,
            sep_token=sep_token,
            pad_token=pad_token,
            cls_token=cls_token,
            mask_token=mask_token,
            **kwargs,
        )

        self.do_lower_case = do_lower_case
