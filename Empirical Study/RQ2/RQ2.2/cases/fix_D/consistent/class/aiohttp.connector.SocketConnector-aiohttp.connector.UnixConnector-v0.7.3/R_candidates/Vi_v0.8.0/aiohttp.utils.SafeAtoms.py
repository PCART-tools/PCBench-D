class SafeAtoms(dict):
    """Copy from gunicorn"""

    def __init__(self, atoms, i_headers, o_headers):
        dict.__init__(self)

        self._i_headers = i_headers
        self._o_headers = o_headers

        for key, value in atoms.items():
            self[key] = value.replace('"', '\\"')

    def __getitem__(self, k):
        if k.startswith('{'):
            if k.endswith('}i'):
                headers = self._i_headers
            elif k.endswith('}o'):
                headers = self._o_headers
            else:
                headers = None

            if headers is not None:
                return headers.get(k[1:-2], '-')

        if k in self:
            return super(SafeAtoms, self).__getitem__(k)
        else:
            return '-'
