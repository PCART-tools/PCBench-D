    def _repr_html_(self) -> str | None:
        """
        Hooks into Jupyter notebook rich display system, which calls _repr_html_ by
        default if an object is returned at the end of a cell.
        """
        if get_option("styler.render.repr") == "html":
            return self.to_html()
        return None
