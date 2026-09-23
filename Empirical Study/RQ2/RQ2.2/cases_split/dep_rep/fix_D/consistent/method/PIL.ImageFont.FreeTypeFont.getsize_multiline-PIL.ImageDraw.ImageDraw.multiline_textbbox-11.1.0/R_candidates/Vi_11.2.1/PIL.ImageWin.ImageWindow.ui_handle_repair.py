    def ui_handle_repair(self, dc: int, x0: int, y0: int, x1: int, y1: int) -> None:
        self.image.draw(dc, (x0, y0, x1, y1))
