    @property
    def max_position_embeddings(self):
        # Message copied from Transformer-XL documentation
        logger.info(f"The model {self.model_type} is one of the few models that has no sequence length limit.")
        return -1
