    def sort(self, *args, **kwargs):
        raise TypeError("cannot sort an Index object in-place, use "
                        "sort_values instead")
