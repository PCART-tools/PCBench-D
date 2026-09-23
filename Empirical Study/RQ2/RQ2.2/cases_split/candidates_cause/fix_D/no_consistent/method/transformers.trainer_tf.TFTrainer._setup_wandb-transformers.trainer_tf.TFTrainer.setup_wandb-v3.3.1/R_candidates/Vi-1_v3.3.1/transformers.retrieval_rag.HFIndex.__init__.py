    def __init__(
        self,
        dataset_name: str,
        dataset_split: str,
        index_name: str,
        vector_size: int,
        index_path: Optional[str] = None,
        use_dummy_dataset=False,
    ):
        super().__init__()
        self.dataset_name = dataset_name
        self.dataset_split = dataset_split
        self.index_name = index_name
        self.vector_size = vector_size
        self.index_path = index_path
        self.use_dummy_dataset = use_dummy_dataset
        self._index_initialize = False

        logger.info("Loading passages from {}".format(self.dataset_name))
        self.dataset = load_dataset(
            self.dataset_name, with_index=False, split=self.dataset_split, dummy=self.use_dummy_dataset
        )
        self.dataset.set_format("numpy", columns=["embeddings"], output_all_columns=True)
