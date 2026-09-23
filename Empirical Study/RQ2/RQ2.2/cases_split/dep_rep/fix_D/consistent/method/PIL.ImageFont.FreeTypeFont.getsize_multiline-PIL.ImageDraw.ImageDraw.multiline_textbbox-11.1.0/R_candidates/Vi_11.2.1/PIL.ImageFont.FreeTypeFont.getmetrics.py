    def getmetrics(self) -> tuple[int, int]:
        """
        :return: A tuple of the font ascent (the distance from the baseline to
            the highest outline point) and descent (the distance from the
            baseline to the lowest outline point, a negative value)
        """
        return self.font.ascent, self.font.descent
