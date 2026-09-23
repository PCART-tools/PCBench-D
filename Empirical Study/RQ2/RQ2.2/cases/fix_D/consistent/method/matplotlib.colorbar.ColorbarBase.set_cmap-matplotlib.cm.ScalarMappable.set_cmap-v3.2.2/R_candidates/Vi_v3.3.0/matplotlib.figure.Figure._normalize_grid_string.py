    @staticmethod
    def _normalize_grid_string(layout):
        layout = inspect.cleandoc(layout)
        return [list(ln) for ln in layout.strip('\n').split('\n')]
