    def post_processor(self):
        return processors.TemplateProcessing(
            single="<s> $A </s>",
            pair="<s> $A </s> </s> $B </s>",
            special_tokens=[
                ("<s>", self.original_tokenizer.convert_tokens_to_ids("<s>")),
                ("</s>", self.original_tokenizer.convert_tokens_to_ids("</s>")),
            ],
        )
