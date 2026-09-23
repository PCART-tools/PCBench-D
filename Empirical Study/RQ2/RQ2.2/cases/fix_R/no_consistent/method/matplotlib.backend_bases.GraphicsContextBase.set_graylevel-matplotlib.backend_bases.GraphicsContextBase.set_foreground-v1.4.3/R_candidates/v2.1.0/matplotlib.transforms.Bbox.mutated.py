    def mutated(self):
        'return whether the bbox has changed since init'
        return self.mutatedx() or self.mutatedy()
