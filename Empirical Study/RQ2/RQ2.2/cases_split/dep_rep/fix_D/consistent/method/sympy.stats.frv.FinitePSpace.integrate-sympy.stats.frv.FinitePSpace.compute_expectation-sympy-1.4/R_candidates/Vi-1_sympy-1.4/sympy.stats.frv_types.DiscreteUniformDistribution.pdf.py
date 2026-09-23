    def pdf(self, x):
        if x in self.args:
            return self.p
        else:
            return S.Zero
