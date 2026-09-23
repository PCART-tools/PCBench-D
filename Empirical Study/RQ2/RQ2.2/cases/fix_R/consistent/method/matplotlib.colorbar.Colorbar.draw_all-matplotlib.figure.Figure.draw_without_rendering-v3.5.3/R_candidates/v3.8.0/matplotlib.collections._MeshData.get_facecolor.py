    def get_facecolor(self):
        # docstring inherited
        # Note that we want to return an array of shape (N*M, 4)
        # a flattened RGBA collection
        return super().get_facecolor().reshape(-1, 4)
