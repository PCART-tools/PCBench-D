    @classmethod
    def draw_if_interactive(cls):
        if cls.trigger_manager_draw is not None and is_interactive():
            manager = Gcf.get_active()
            if manager:
                cls.trigger_manager_draw(manager)
