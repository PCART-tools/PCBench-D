    def save_pretrained(self, save_directory):
        logger.warning(
            "Please note you will not be able to load the vocabulary in"
            " Python-based TransfoXLTokenizer as they don't share the same structure."
        )

        return super().save_pretrained(save_directory)
