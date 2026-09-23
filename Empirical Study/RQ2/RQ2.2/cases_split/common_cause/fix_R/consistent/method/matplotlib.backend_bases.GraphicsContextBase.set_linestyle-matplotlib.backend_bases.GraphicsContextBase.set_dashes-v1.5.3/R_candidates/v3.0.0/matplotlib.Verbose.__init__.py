    @cbook.deprecated("2.2", message=_verbose_msg)
    def __init__(self):
        self.set_level('silent')
        self.fileo = sys.stdout
