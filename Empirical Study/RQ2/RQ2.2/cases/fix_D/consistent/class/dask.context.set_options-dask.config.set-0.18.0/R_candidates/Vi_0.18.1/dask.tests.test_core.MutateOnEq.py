class MutateOnEq(object):
    hit_eq = 0

    def __eq__(self, other):
        self.hit_eq += 1
        return False
