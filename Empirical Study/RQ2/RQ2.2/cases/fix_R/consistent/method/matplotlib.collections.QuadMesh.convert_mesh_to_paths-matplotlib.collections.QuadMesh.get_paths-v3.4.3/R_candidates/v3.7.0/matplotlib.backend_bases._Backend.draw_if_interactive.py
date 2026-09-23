    @classmethod
    def draw_if_interactive(cls):
        manager_class = cls.FigureCanvas.manager_class
        # Interactive backends reimplement start_main_loop or pyplot_show.
        backend_is_interactive = (
            manager_class.start_main_loop != FigureManagerBase.start_main_loop
            or manager_class.pyplot_show != FigureManagerBase.pyplot_show)
        if backend_is_interactive and is_interactive():
            manager = Gcf.get_active()
            if manager:
                manager.canvas.draw_idle()
