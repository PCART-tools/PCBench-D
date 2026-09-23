    def remove(self, o):
        'remove element *o* from the stack'
        if o not in self._elements:
            raise ValueError('Unknown element o')
        old = self._elements[:]
        self.clear()
        for thiso in old:
            if thiso == o:
                continue
            else:
                self.push(thiso)
