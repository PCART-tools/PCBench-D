    def post_processor(self):
        return processors.TemplateProcessing(
            single="$A </s> en_XX",
            pair="$A $B </s> en_XX",
            special_tokens=[
                ("en_XX", self.original_tokenizer.convert_tokens_to_ids("en_XX")),
                ("</s>", self.original_tokenizer.convert_tokens_to_ids("</s>")),
            ],
        )
