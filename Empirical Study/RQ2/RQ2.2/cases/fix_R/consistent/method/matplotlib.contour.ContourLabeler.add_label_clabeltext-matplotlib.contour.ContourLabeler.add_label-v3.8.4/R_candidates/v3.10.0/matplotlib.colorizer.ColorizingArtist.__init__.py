    def __init__(self, colorizer, **kwargs):
        """
        Parameters
        ----------
        colorizer : `.colorizer.Colorizer`
        """
        _api.check_isinstance(Colorizer, colorizer=colorizer)
        super().__init__(colorizer=colorizer, **kwargs)
