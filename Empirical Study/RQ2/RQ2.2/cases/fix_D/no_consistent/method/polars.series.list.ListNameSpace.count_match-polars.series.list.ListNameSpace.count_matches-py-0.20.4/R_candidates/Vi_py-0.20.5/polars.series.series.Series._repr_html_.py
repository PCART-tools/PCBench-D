    def _repr_html_(self) -> str:
        """Format output data in HTML for display in Jupyter Notebooks."""
        return self.to_frame()._repr_html_(from_series=True)
