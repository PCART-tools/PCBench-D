    def argsort(self, *args, **kwargs):
        return np.lexsort((self.right, self.left))
