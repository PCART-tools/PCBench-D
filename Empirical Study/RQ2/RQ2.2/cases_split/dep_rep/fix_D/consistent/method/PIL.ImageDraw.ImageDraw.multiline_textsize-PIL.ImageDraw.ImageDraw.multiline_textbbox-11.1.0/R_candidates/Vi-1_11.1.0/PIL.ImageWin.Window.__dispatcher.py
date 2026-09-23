    def __dispatcher(self, action: str, *args: int) -> None:
        getattr(self, f"ui_handle_{action}")(*args)
