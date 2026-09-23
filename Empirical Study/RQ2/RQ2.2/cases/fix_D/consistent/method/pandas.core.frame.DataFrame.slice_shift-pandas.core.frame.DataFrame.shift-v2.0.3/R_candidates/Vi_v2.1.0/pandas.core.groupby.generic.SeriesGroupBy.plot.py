    @property
    @doc(Series.plot.__doc__)
    def plot(self):
        result = GroupByPlot(self)
        return result
