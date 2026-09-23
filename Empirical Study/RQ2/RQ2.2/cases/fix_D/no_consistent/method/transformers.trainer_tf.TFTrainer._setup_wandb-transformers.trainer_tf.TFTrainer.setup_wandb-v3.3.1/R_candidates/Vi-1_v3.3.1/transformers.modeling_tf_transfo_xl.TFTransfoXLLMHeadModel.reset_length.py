    def reset_length(self, tgt_len, ext_len, mem_len):
        warnings.warn(
            "The method `reset_length` is deprecated and will be removed in a future version, use `reset_memory_length` instead.",
            FutureWarning,
        )
        self.transformer.reset_memory_length(mem_len)
