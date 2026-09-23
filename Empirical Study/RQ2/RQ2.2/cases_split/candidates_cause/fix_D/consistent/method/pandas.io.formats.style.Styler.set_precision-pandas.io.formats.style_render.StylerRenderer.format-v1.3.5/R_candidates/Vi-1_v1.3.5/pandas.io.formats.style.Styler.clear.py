    def clear(self) -> None:
        """
        Reset the ``Styler``, removing any previously applied styles.

        Returns None.
        """
        self.ctx.clear()
        self.tooltips = None
        self.cell_context.clear()
        self._todo.clear()

        self.hide_index_ = False
        self.hidden_columns = []
