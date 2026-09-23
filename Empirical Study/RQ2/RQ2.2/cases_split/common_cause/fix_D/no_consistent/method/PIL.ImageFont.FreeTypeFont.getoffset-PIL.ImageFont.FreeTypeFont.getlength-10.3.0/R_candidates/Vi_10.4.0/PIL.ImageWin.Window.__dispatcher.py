    def __dispatcher(self, action, *args):
        return getattr(self, f"ui_handle_{action}")(*args)
