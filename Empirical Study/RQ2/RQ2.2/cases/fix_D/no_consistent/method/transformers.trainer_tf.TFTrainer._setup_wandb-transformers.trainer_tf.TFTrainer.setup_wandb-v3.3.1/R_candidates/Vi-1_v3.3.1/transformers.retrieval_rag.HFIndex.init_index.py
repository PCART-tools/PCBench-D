    def init_index(self):
        if self.index_path is not None:
            logger.info("Loading index from {}".format(self.index_path))
            self.index.load_faiss_index(index_name=self.index_name, file=self.index_path)
        else:
            logger.info("Loading index from {}".format(self.dataset_name + " with index name " + self.index_name))
            self.dataset = load_dataset(
                self.dataset_name,
                with_embeddings=True,
                with_index=True,
                split=self.dataset_split,
                index_name=self.index_name,
                dummy=self.use_dummy_dataset,
            )
            self.dataset.set_format("numpy", columns=["embeddings"], output_all_columns=True)
        self._index_initialize = True
