    def __init__(
        self,
        vector_size: int,
        dataset_name: str = "wiki_dpr",
        dataset_split: str = "train",
        index_name: Optional[str] = None,
        index_path: Optional[str] = None,
        use_dummy_dataset=False,
    ):
        if int(index_path is None) + int(index_name is None) != 1:
            raise ValueError("Please provide `index_name` or `index_path`.")
        self.dataset_name = dataset_name
        self.dataset_split = dataset_split
        self.index_name = index_name
        self.index_path = index_path
        self.use_dummy_dataset = use_dummy_dataset
        logger.info("Loading passages from {}".format(self.dataset_name))
        dataset = load_dataset(
            self.dataset_name, with_index=False, split=self.dataset_split, dummy=self.use_dummy_dataset
        )
        super().__init__(vector_size, dataset, index_initialized=False)
