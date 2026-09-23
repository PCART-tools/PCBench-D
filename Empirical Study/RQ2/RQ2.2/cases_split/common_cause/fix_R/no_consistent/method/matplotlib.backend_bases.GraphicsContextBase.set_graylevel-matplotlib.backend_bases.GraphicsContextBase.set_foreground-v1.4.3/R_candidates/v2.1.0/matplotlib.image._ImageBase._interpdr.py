    @cbook.deprecated("2.1")
    def _interpdr(self):
        return {v: k for k, v in six.iteritems(_interpd_)}
