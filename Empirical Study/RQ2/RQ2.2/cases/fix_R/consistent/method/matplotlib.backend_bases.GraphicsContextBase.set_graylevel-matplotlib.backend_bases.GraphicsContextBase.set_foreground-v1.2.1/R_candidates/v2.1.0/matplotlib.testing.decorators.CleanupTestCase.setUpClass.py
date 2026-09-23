    @classmethod
    def setUpClass(cls):
        import matplotlib.units
        cls.original_units_registry = matplotlib.units.registry.copy()
        cls.original_settings = mpl.rcParams.copy()
