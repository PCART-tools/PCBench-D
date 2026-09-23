    def converted(self) -> Tokenizer:
        vocab = self.original_tokenizer.vocab
        tokenizer = Tokenizer(WordPiece(vocab, unk_token=str(self.original_tokenizer.unk_token)))

        # # Let the tokenizer know about special tokens if they are part of the vocab
        # if tokenizer.token_to_id(str(self.original_tokenizer.unk_token)) is not None:
        #     tokenizer.add_special_tokens([str(self.original_tokenizer.unk_token)])
        # if tokenizer.token_to_id(str(self.original_tokenizer.sep_token)) is not None:
        #     tokenizer.add_special_tokens([str(self.original_tokenizer.sep_token)])
        # if tokenizer.token_to_id(str(self.original_tokenizer.cls_token)) is not None:
        #     tokenizer.add_special_tokens([str(self.original_tokenizer.cls_token)])
        # if tokenizer.token_to_id(str(self.original_tokenizer.pad_token)) is not None:
        #     tokenizer.add_special_tokens([str(self.original_tokenizer.pad_token)])
        # if tokenizer.token_to_id(str(self.original_tokenizer.mask_token)) is not None:
        #     tokenizer.add_special_tokens([str(self.original_tokenizer.mask_token)])

        tokenize_chinese_chars = False
        strip_accents = False
        do_lower_case = False
        if hasattr(self.original_tokenizer, "basic_tokenizer"):
            tokenize_chinese_chars = self.original_tokenizer.basic_tokenizer.tokenize_chinese_chars
            strip_accents = self.original_tokenizer.basic_tokenizer.strip_accents
            do_lower_case = self.original_tokenizer.basic_tokenizer.do_lower_case

        tokenizer.normalizer = normalizers.BertNormalizer(
            clean_text=True,
            handle_chinese_chars=tokenize_chinese_chars,
            strip_accents=strip_accents,
            lowercase=do_lower_case,
        )
        tokenizer.pre_tokenizer = pre_tokenizers.BertPreTokenizer()

        cls = str(self.original_tokenizer.cls_token)
        sep = str(self.original_tokenizer.sep_token)
        cls_token_id = self.original_tokenizer.cls_token_id
        sep_token_id = self.original_tokenizer.sep_token_id

        tokenizer.post_processor = processors.TemplateProcessing(
            single=f"{cls}:0 $A:0 {sep}:0",
            pair=f"{cls}:0 $A:0 {sep}:0 $B:1 {sep}:1",
            special_tokens=[
                (cls, cls_token_id),
                (sep, sep_token_id),
            ],
        )
        tokenizer.decoder = decoders.WordPiece(prefix="##")

        return tokenizer
