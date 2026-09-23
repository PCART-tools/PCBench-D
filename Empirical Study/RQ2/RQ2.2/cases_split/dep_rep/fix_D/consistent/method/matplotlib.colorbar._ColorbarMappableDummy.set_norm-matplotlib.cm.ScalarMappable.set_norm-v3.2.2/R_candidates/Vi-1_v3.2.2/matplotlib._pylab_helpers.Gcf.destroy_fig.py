    @classmethod
    def destroy_fig(cls, fig):
        "*fig* is a Figure instance"
        num = next((manager.num for manager in cls.figs.values()
                    if manager.canvas.figure == fig), None)
        if num is not None:
            cls.destroy(num)
