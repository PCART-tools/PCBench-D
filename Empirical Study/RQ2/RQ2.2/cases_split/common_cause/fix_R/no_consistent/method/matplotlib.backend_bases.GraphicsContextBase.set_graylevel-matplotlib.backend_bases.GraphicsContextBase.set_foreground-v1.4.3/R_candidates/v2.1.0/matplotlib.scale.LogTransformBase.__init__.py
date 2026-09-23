    def __init__(self, nonpos):
        Transform.__init__(self)
        if nonpos == 'mask':
            self._fill_value = np.nan
        else:
            self._fill_value = 1e-300
