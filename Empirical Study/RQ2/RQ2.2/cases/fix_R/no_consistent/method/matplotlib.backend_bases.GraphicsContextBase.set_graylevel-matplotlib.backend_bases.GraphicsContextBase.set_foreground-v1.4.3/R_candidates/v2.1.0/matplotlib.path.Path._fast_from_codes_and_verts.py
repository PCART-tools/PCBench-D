    @classmethod
    def _fast_from_codes_and_verts(cls, verts, codes, internals=None):
        """
        Creates a Path instance without the expense of calling the constructor

        Parameters
        ----------
        verts : numpy array
        codes : numpy array
        internals : dict or None
            The attributes that the resulting path should have.
            Allowed keys are ``readonly``, ``should_simplify``,
            ``simplify_threshold``, ``has_nonfinite`` and
            ``interpolation_steps``.

        """
        internals = internals or {}
        pth = cls.__new__(cls)
        pth._vertices = _to_unmasked_float_array(verts)
        pth._codes = codes
        pth._readonly = internals.pop('readonly', False)
        pth.should_simplify = internals.pop('should_simplify', True)
        pth.simplify_threshold = (
            internals.pop('simplify_threshold',
                          rcParams['path.simplify_threshold'])
        )
        pth._has_nonfinite = internals.pop('has_nonfinite', False)
        pth._interpolation_steps = internals.pop('interpolation_steps', 1)
        if internals:
            raise ValueError('Unexpected internals provided to '
                             '_fast_from_codes_and_verts: '
                             '{0}'.format('\n *'.join(internals)))
        return pth
