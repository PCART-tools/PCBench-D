    def _repr_pretty_(self, p: PrettyPrinter, cycle: bool) -> None:
        """IPython plain text display support"""

        # Same as __repr__ but without unpredictable id(self),
        # to keep Jupyter notebook `text/plain` output stable.
        p.text(
            "<%s.%s image mode=%s size=%dx%d>"
            % (
                self.__class__.__module__,
                self.__class__.__name__,
                self.mode,
                self.size[0],
                self.size[1],
            )
        )
