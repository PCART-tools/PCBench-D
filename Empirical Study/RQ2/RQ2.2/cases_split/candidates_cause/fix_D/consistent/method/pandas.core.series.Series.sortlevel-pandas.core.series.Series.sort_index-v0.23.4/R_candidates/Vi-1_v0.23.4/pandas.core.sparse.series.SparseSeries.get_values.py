    def get_values(self):
        """ same as values """
        return self.block.to_dense().view()
