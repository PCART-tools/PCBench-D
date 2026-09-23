    def marginal_distribution(self, *indices):
        count = self.component_count
        orig = [Indexed(self.symbol, i) for i in range(count)]
        all_syms = [Symbol(str(i)) for i in orig]
        replace_dict = dict(zip(all_syms, orig))
        sym = [Symbol(str(Indexed(self.symbol, i))) for i in indices]
        limits = list([i,] for i in all_syms if i not in sym)
        index = 0
        for i in range(count):
            if i not in indices:
                limits[index].append(self.distribution.set.args[i])
                limits[index] = tuple(limits[index])
                index += 1
        limits = tuple(limits)
        if self.distribution.is_Continuous:
            f = Lambda(sym, integrate(self.distribution(*all_syms), limits))
        elif self.distribution.is_Discrete:
            f = Lambda(sym, summation(self.distribution(all_syms), limits))
        return f.xreplace(replace_dict)
