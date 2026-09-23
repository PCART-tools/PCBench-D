    def __init__(self, fh):
        """Parse the AFM file in file object *fh*."""
        (self._header,
         self._metrics,
         self._metrics_by_name,
         self._kern,
         self._composite) = _parse_afm(fh)
