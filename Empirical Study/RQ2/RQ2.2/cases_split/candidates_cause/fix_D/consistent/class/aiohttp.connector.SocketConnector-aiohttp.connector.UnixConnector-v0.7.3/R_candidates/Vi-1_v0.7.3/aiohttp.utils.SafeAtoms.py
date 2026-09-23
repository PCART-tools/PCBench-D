class SafeAtoms(dict):
    """Copy from gunicorn"""

    def __init__(self, atoms):
        dict.__init__(self)
        for key, value in atoms.items():
            self[key] = value.replace('"', '\\"')

    def __getitem__(self, k):
        if k.startswith("{"):
            kl = k.lower()
            if kl in self:
                return super(SafeAtoms, self).__getitem__(kl)
            else:
                return "-"
        if k in self:
            return super(SafeAtoms, self).__getitem__(k)
        else:
            return '-'
