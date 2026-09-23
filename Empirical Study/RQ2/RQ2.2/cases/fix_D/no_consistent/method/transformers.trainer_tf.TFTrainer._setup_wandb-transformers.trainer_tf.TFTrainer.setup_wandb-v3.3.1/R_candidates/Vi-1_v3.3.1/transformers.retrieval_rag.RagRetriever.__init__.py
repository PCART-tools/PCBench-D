    def __init__(self, config, question_encoder_tokenizer, generator_tokenizer):
        super().__init__()
        self.index = (
            LegacyIndex(
                config.retrieval_vector_size,
                config.index_path or LEGACY_INDEX_PATH,
            )
            if config.index_name == "legacy"
            else HFIndex(
                config.dataset,
                config.dataset_split,
                config.index_name,
                config.retrieval_vector_size,
                config.index_path,
                config.use_dummy_dataset,
            )
        )
        self.generator_tokenizer = generator_tokenizer
        self.question_encoder_tokenizer = question_encoder_tokenizer

        self.n_docs = config.n_docs
        self.batch_size = config.retrieval_batch_size

        self.config = config
        if self._init_retrieval:
            self.init_retrieval()
