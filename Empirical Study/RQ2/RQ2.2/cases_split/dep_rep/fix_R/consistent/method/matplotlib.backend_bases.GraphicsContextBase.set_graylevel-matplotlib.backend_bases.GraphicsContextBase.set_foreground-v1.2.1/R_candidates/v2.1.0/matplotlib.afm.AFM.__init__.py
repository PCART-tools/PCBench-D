    def __init__(self, fh):
        """
        Parse the AFM file in file object *fh*
        """
        (dhead, dcmetrics_ascii, dcmetrics_name, dkernpairs, dcomposite) = \
            parse_afm(fh)
        self._header = dhead
        self._kern = dkernpairs
        self._metrics = dcmetrics_ascii
        self._metrics_by_name = dcmetrics_name
        self._composite = dcomposite
