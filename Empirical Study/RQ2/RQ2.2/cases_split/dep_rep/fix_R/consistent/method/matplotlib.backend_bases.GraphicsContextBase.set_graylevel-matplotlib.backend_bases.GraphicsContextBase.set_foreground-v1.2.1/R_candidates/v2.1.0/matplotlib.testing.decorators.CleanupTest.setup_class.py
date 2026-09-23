    @classmethod
    def setup_class(cls):
        cls.original_units_registry = matplotlib.units.registry.copy()
        cls.original_settings = mpl.rcParams.copy()
        matplotlib.testing.setup()
