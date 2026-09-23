    def transposed(self):
        """
        Transposes the colormap by swapping the order of the axis
        """
        return self.resampled((None, None), transposed=True)
