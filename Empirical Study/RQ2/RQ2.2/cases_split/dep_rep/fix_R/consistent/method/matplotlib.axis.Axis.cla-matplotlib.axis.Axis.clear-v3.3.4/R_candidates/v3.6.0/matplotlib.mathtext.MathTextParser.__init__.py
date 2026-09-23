    def __init__(self, output):
        """
        Create a MathTextParser for the given backend *output*.

        Parameters
        ----------
        output : {"path", "agg"}
            Whether to return a `VectorParse` ("path") or a
            `RasterParse` ("agg", or its synonym "macosx").
        """
        self._output_type = _api.check_getitem(
            {"path": "vector", "agg": "raster", "macosx": "raster"},
            output=output.lower())
