    @n_token.setter
    def n_token(self, value):  # Backward compatibility
        self.vocab_size = value
