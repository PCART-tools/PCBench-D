    def add_child(self, child, i=0, j=0):
        # np.ix_ returns the cross product of i and j indices
        self.children[np.ix_(np.atleast_1d(i), np.atleast_1d(j))] = child
