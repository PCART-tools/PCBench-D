    def __init__(self, rel, reverse=False):
        super(ManyToManyDescriptor, self).__init__(rel)

        self.reverse = reverse
