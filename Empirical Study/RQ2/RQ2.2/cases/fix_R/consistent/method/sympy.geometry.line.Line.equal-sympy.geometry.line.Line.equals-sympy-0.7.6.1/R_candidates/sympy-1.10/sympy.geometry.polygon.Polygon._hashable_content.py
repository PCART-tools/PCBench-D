    def _hashable_content(self):

        D = {}
        def ref_list(point_list):
            kee = {}
            for i, p in enumerate(ordered(set(point_list))):
                kee[p] = i
                D[i] = p
            return [kee[p] for p in point_list]

        S1 = ref_list(self.args)
        r_nor = rotate_left(S1, least_rotation(S1))
        S2 = ref_list(list(reversed(self.args)))
        r_rev = rotate_left(S2, least_rotation(S2))
        if r_nor < r_rev:
            r = r_nor
        else:
            r = r_rev
        canonical_args = [ D[order] for order in r ]
        return tuple(canonical_args)
