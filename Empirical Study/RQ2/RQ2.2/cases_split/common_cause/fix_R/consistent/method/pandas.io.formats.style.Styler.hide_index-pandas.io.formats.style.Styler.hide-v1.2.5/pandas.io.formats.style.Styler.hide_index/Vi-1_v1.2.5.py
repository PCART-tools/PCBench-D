    def hide_index(self) -> "Styler":
        """
        Hide any indices from rendering.

        Returns
        -------
        self : Styler
        """
        self.hidden_index = True
        return self
