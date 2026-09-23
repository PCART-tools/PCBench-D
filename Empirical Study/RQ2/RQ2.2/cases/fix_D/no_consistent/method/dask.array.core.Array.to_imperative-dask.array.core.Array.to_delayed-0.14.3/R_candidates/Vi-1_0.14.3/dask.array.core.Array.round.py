    @wraps(np.round)
    def round(self, decimals=0):
        return round(self, decimals=decimals)
