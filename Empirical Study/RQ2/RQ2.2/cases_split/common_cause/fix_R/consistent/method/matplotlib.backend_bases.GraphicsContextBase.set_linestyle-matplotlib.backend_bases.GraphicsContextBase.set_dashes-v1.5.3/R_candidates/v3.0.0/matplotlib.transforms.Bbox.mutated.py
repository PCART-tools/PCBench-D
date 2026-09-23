    def mutated(self):
        'Return whether the bbox has changed since init.'
        return self.mutatedx() or self.mutatedy()
