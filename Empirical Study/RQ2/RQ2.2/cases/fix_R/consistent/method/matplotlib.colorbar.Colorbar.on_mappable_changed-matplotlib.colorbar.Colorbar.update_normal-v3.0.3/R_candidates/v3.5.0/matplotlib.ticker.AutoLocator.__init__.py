    def __init__(self):
        """
        To know the values of the non-public parameters, please have a
        look to the defaults of `~matplotlib.ticker.MaxNLocator`.
        """
        if mpl.rcParams['_internal.classic_mode']:
            nbins = 9
            steps = [1, 2, 5, 10]
        else:
            nbins = 'auto'
            steps = [1, 2, 2.5, 5, 10]
        super().__init__(nbins=nbins, steps=steps)
