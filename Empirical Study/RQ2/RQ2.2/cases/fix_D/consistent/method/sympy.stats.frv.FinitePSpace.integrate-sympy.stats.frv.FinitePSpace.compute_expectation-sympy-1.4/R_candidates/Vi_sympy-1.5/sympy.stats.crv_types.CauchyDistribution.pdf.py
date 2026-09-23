    def pdf(self, x):
        return 1/(pi*self.gamma*(1 + ((x - self.x0)/self.gamma)**2))
