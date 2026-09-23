    def save_pretrained(self, save_directory):
        self.config.save_pretrained(save_directory)
        rag_tokenizer = RagTokenizer(
            question_encoder=self.question_encoder_tokenizer,
            generator=self.generator_tokenizer,
        )
        rag_tokenizer.save_pretrained(save_directory)
