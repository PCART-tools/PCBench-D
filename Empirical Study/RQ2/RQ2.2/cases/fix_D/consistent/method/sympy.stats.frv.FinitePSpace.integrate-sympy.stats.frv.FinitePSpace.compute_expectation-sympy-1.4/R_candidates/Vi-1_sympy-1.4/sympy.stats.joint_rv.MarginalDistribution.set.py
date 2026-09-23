    @property
    def set(self):
        rvs = [i for i in random_symbols(self.args[1])]
        marginalise_out = [i for i in random_symbols(self.args[1]) \
         if i not in self.args[1]]
        for i in rvs:
            if i in marginalise_out:
                rvs.remove(i)
        return ProductSet((i.pspace.set for i in rvs))
