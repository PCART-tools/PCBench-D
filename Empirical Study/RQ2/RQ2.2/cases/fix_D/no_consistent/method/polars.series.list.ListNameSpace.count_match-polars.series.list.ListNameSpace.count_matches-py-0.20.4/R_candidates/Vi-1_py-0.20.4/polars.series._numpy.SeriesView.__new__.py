    def __new__(
        cls, input_array: np.ndarray[Any, Any], owned_series: Series
    ) -> SeriesView:
        # Input array is an already formed ndarray instance
        # We first cast to be our class type
        obj = input_array.view(cls)
        # add the new attribute to the created instance
        obj.owned_series = owned_series
        # Finally, we must return the newly created object:
        return obj
