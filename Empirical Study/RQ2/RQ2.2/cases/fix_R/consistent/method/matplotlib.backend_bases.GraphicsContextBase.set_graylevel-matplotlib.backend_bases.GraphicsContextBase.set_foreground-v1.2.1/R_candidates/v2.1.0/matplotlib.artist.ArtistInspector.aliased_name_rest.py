    def aliased_name_rest(self, s, target):
        """
        return 'PROPNAME or alias' if *s* has an alias, else return
        PROPNAME formatted for ReST

        e.g., for the line markerfacecolor property, which has an
        alias, return 'markerfacecolor or mfc' and for the transform
        property, which does not, return 'transform'
        """

        if s in self.aliasd:
            aliases = ''.join([' or %s' % x
                               for x in sorted(self.aliasd[s])])
        else:
            aliases = ''
        return ':meth:`%s <%s>`%s' % (s, target, aliases)
