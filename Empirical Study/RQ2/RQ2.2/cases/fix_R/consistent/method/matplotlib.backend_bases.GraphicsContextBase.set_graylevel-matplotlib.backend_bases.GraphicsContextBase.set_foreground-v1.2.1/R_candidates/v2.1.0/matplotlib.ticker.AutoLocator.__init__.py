    def __init__(self):
        if rcParams['_internal.classic_mode']:
            nbins = 9
            steps = [1, 2, 5, 10]
        else:
            nbins = 'auto'
            steps = [1, 2, 2.5, 5, 10]
        MaxNLocator.__init__(self, nbins=nbins, steps=steps)
