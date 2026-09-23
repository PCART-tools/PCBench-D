    def _select_iterator(self, over: str) -> type[RowStringIterator]:
        """Select proper iterator over table rows."""
        if over == "header":
            return RowHeaderIterator
        elif over == "body":
            return RowBodyIterator
        else:
            msg = f"'over' must be either 'header' or 'body', but {over} was provided"
            raise ValueError(msg)
