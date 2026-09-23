    def getname(self) -> tuple[str | None, str | None]:
        """
        :return: A tuple of the font family (e.g. Helvetica) and the font style
            (e.g. Bold)
        """
        return self.font.family, self.font.style
