    def __init__(self, values, placement, ndim=None):
        # coerce to categorical if we can
        values = extract_array(values)
        assert isinstance(values, Categorical), type(values)
        super().__init__(values, placement=placement, ndim=ndim)
