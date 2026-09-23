    def _get_baseline(self, filename):
        if dict.__getitem__(rcParams, 'text.latex.preview'):
            baseline = Path(filename).with_suffix(".baseline")
            if baseline.exists():
                height, depth, width = baseline.read_bytes().split()
                return float(depth)
        return None
