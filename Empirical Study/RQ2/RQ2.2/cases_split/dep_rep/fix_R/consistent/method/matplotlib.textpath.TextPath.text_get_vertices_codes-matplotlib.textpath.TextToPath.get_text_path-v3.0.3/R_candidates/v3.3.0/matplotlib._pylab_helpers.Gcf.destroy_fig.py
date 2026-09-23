    @classmethod
    def destroy_fig(cls, fig):
        """Destroy figure *fig*."""
        canvas = getattr(fig, "canvas", None)
        manager = getattr(canvas, "manager", None)
        cls.destroy(manager)
