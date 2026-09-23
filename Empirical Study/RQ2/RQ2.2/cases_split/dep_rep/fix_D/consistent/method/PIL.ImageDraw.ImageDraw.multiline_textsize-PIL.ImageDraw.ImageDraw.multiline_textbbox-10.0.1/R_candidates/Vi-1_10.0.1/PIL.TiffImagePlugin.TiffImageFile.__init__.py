    def __init__(self, fp=None, filename=None):
        self.tag_v2 = None
        """ Image file directory (tag dictionary) """

        self.tag = None
        """ Legacy tag entries """

        super().__init__(fp, filename)
