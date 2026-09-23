    @classmethod
    def from_pretrained(cls, retriever_name_or_path, **kwargs):
        config = RagConfig.from_pretrained(retriever_name_or_path, **kwargs)
        rag_tokenizer = RagTokenizer.from_pretrained(retriever_name_or_path, config=config)
        question_encoder_tokenizer = rag_tokenizer.question_encoder
        generator_tokenizer = rag_tokenizer.generator
        return cls(
            config, question_encoder_tokenizer=question_encoder_tokenizer, generator_tokenizer=generator_tokenizer
        )
