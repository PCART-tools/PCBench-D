    def _checkdim(self, dim):
        "Check the given dimension."
        if dim < 0 or dim > 2:
            raise GEOSException('invalid ordinate dimension "%d"' % dim)
