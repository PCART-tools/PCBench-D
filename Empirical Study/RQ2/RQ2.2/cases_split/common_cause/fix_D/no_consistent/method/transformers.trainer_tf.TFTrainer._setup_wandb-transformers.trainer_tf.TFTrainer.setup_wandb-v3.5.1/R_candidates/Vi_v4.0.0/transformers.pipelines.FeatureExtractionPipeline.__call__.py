    def __call__(self, *args, **kwargs):
        """
        Extract the features of the input(s).

        Args:
            args (:obj:`str` or :obj:`List[str]`): One or several texts (or one list of texts) to get the features of.

        Return:
            A nested list of :obj:`float`: The features computed by the model.
        """
        return super().__call__(*args, **kwargs).tolist()
