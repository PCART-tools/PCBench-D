    @property
    def _label_macro(self) -> str:
        r"""Label macro, extracted from self.label, like \label{ref}."""
        return f"\\label{{{self.label}}}" if self.label else ""
