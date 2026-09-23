    @cbook.deprecated("2.2", message=_verbose_msg)
    def set_fileo(self, fname):
        std = {
            'sys.stdout': sys.stdout,
            'sys.stderr': sys.stderr,
        }
        if fname in std:
            self.fileo = std[fname]
        else:
            try:
                fileo = open(fname, 'w')
            except IOError:
                raise ValueError('Verbose object could not open log file "{0}"'
                                 ' for writing.\nCheck your matplotlibrc '
                                 'verbose.fileo setting'.format(fname))
            else:
                self.fileo = fileo
