    @classmethod
    def from_pretrained(cls, pretrained_model_name_or_path, **kwargs):
        # dynamically import AutoTokenizer
        from .tokenization_auto import AutoTokenizer

        config = kwargs.pop("config", None)

        if config is None:
            config = RagConfig.from_pretrained(pretrained_model_name_or_path)

        question_encoder_path = os.path.join(pretrained_model_name_or_path, "question_encoder_tokenizer")
        generator_path = os.path.join(pretrained_model_name_or_path, "generator_tokenizer")
        question_encoder = AutoTokenizer.from_pretrained(question_encoder_path, config=config.question_encoder)
        generator = AutoTokenizer.from_pretrained(generator_path, config=config.generator)
        return cls(question_encoder=question_encoder, generator=generator)
