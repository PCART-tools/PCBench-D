    def set_parent(self, parent):
        ''' replace the parent of this with the new parent
        '''
        self.parent = parent
        self.parent_constrain()
