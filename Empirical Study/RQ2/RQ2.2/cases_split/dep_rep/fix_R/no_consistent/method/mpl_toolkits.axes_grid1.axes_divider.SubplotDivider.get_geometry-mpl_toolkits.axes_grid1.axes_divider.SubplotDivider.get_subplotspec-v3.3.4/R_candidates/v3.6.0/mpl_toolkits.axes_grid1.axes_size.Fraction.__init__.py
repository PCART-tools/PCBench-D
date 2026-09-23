    def __init__(self, fraction, ref_size):
        _api.check_isinstance(Number, fraction=fraction)
        self._fraction_ref = ref_size
        self._fraction = fraction
