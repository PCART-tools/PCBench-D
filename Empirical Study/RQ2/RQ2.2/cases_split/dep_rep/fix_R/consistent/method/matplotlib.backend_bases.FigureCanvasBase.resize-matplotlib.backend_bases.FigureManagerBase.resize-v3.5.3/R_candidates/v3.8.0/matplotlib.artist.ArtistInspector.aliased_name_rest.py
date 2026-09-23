    def aliased_name_rest(self, s, target):
        """
        Return 'PROPNAME or alias' if *s* has an alias, else return 'PROPNAME',
        formatted for reST.

        For example, for the line markerfacecolor property, which has an
        alias, return 'markerfacecolor or mfc' and for the transform
        property, which does not, return 'transform'.
        """
        # workaround to prevent "reference target not found"
        if target in self._NOT_LINKABLE:
            return f'``{s}``'

        aliases = ''.join(' or %s' % x for x in sorted(self.aliasd.get(s, [])))
        return f':meth:`{s} <{target}>`{aliases}'
