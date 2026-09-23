    def constrain_height(self, height, strength='strong'):
        '''
        Constrain the height of the layout box.  height is
        either a float or a layoutbox.height.
        '''
        c = (self.height == height)
        self.solver.addConstraint(c | strength)
