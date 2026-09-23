    def __init__(self, config):
        super().__init__(config)
        assert config.is_decoder, "If you want to use `ReformerModelWithLMHead` make sure that `is_decoder=True`."
        assert (
            "local" not in self.config.attn_layers or config.local_num_chunks_after == 0
        ), f"If causal mask is enabled, make sure that `config.local_num_chunks_after` is set to 0 and not {config.local_num_chunks_after}."
        assert (
            "lsh" not in self.config.attn_layers or config.lsh_num_chunks_after == 0
        ), f"If causal mask is enabled, make sure that `config.lsh_num_chunks_after` is set to 1 and not {config.lsh_num_chunks_after}."

        self.reformer = ReformerModel(config)
        self.lm_head = ReformerOnlyLMHead(config)

        self.init_weights()
