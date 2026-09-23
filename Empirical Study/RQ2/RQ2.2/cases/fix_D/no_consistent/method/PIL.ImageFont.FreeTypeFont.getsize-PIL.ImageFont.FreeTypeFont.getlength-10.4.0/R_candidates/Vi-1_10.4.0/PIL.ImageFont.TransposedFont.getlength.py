    def getlength(self, text: str | bytes, *args, **kwargs) -> float:
        if self.orientation in (Image.Transpose.ROTATE_90, Image.Transpose.ROTATE_270):
            msg = "text length is undefined for text rotated by 90 or 270 degrees"
            raise ValueError(msg)
        return self.font.getlength(text, *args, **kwargs)
