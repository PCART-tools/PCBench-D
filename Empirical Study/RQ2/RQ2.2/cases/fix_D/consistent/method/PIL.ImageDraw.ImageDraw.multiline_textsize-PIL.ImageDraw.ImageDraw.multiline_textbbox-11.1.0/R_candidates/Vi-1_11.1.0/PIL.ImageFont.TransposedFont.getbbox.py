    def getbbox(
        self, text: str | bytes, *args: Any, **kwargs: Any
    ) -> tuple[int, int, float, float]:
        # TransposedFont doesn't support getmask2, move top-left point to (0, 0)
        # this has no effect on ImageFont and simulates anchor="lt" for FreeTypeFont
        left, top, right, bottom = self.font.getbbox(text, *args, **kwargs)
        width = right - left
        height = bottom - top
        if self.orientation in (Image.Transpose.ROTATE_90, Image.Transpose.ROTATE_270):
            return 0, 0, height, width
        return 0, 0, width, height
