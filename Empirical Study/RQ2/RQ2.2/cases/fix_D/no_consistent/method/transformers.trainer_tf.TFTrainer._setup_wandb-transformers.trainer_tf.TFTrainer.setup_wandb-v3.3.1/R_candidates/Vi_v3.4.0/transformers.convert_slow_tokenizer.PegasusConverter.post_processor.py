    def post_processor(self):
        eos = self.original_tokenizer.eos_token
        return processors.TemplateProcessing(
            single=["$A", eos],
            pair=["$A", "$B", eos],
            special_tokens=[
                (eos, self.original_tokenizer.eos_token_id),
            ],
        )
