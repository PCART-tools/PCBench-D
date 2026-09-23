    @classmethod
    def create_with_canvas(cls, canvas_class, figure, num):
        canvas = canvas_class(figure)
        manager = cls(canvas, num)
        if is_interactive():
            manager.show()
            canvas.draw_idle()

        def destroy(event):
            canvas.mpl_disconnect(cid)
            Gcf.destroy(manager)

        cid = canvas.mpl_connect('close_event', destroy)
        return manager
