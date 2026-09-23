    def _repr_pretty_(self, p: PrettyPrinter, cycle: bool) -> None:
        """IPython plain text display support"""

        # Same as __repr__ but without unpredictable id(self),
        # to keep Jupyter notebook `text/plain` output stable.
        p.text(
            f"<{self.__class__.__module__}.{self.__class__.__name__} "
            f"image mode={self.mode} size={self.size[0]}x{self.size[1]}>"
        )
