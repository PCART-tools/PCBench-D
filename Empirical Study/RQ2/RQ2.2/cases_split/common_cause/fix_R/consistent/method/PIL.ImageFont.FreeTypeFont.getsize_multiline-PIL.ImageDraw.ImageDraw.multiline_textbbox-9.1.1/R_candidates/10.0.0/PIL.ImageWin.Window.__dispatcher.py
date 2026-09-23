    def __dispatcher(self, action, *args):
        return getattr(self, "ui_handle_" + action)(*args)
