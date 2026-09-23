    def _repr_html_(self) -> str:
        """
        Hooks into Jupyter notebook rich display system.
        """
        return self.render()
