def get_splitter(data, *args, **kwargs):
    if isinstance(data, Series):
        klass = SeriesSplitter
    elif isinstance(data, DataFrame):
        klass = FrameSplitter
    else:
        klass = NDFrameSplitter

    return klass(data, *args, **kwargs)
