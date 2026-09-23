    def sort(self, *args, **kwargs):
        """
        Use sort_values instead.
        """
        raise TypeError(
            "cannot sort an Index object in-place, use " "sort_values instead"
        )
