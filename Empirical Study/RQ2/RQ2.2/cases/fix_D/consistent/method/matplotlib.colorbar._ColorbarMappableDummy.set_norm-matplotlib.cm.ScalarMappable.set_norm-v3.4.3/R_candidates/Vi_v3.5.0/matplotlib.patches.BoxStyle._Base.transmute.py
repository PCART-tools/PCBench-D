        @_api.deprecated("3.4")
        def transmute(self, x0, y0, width, height, mutation_size):
            """Return the `~.path.Path` outlining the given rectangle."""
            return self(self, x0, y0, width, height, mutation_size, 1)
