    @abc.abstractmethod
    def wrap_results_for_axis(
        self, results: ResType, res_index: "Index"
    ) -> Union["Series", "DataFrame"]:
        pass
