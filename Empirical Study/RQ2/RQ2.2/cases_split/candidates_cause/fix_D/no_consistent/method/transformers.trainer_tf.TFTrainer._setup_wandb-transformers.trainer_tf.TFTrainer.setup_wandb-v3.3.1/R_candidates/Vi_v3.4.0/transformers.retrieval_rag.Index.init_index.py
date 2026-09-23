    def init_index(self):
        """
        A function responsible for loading the index into memory. Should be called only once per training run of a RAG model.
        E.g. if the model is trained on multiple GPUs in a distributed setup, only one of the workers will load the index.
        """
        raise NotImplementedError
