    def aliased_name(self, s):
        """
        return 'PROPNAME or alias' if *s* has an alias, else return
        PROPNAME.

        e.g., for the line markerfacecolor property, which has an
        alias, return 'markerfacecolor or mfc' and for the transform
        property, which does not, return 'transform'
        """

        if s in self.aliasd:
            return s + ''.join([' or %s' % x
                                for x in sorted(self.aliasd[s])])
        else:
            return s
