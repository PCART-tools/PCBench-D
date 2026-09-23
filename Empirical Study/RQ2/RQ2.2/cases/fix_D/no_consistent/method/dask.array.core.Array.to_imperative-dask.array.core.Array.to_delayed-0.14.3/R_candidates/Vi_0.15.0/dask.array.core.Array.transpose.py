    @derived_from(np.ndarray)
    def transpose(self, *axes):
        if not axes:
            axes = None
        elif len(axes) == 1 and isinstance(axes[0], Iterable):
            axes = axes[0]
        return transpose(self, axes=axes)
