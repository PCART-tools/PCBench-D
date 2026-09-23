    def sort(self, cmp=None, key=None, reverse=False):
        "Standard list sort method"
        if key:
            temp = [(key(v), v) for v in self]
            temp.sort(key=lambda x: x[0], reverse=reverse)
            self[:] = [v[1] for v in temp]
        else:
            temp = list(self)
            if cmp is not None:
                temp.sort(cmp=cmp, reverse=reverse)
            else:
                temp.sort(reverse=reverse)
            self[:] = temp
