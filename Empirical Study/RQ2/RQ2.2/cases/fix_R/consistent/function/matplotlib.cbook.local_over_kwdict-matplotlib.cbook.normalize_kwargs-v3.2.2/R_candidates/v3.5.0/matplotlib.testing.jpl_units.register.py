def register():
    """Register the unit conversion classes with matplotlib."""
    import matplotlib.units as mplU

    mplU.registry[str] = StrConverter()
    mplU.registry[Epoch] = EpochConverter()
    mplU.registry[Duration] = EpochConverter()
    mplU.registry[UnitDbl] = UnitDblConverter()
