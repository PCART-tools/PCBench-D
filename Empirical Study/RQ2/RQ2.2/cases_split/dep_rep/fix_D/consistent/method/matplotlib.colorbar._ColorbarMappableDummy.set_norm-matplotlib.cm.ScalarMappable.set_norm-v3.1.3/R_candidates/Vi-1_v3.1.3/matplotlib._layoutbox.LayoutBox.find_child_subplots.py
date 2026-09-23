    def find_child_subplots(self):
        '''
        Find children of this layout box that are subplots.  We want to line
        poss up, and this is an easy way to find them all.
        '''
        if self.subplot:
            subplots = [self]
        else:
            subplots = []
        for child in self.children:
            subplots += child.find_child_subplots()
        return subplots
