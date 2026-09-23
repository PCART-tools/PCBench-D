    def post_processor(self):
        return processors.TemplateProcessing(
            single="$A:0 <sep>:0 <cls>:2",
            pair="$A:0 <sep>:0 $B:1 <sep>:1 <cls>:2",
            special_tokens=[
                ("<sep>", self.original_tokenizer.convert_tokens_to_ids("<sep>")),
                ("<cls>", self.original_tokenizer.convert_tokens_to_ids("<cls>")),
            ],
        )
