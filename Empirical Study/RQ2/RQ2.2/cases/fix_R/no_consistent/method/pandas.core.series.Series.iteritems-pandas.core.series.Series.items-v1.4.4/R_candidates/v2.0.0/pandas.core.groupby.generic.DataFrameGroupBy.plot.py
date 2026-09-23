    @property
    @doc(DataFrame.plot.__doc__)
    def plot(self) -> GroupByPlot:
        result = GroupByPlot(self)
        return result
