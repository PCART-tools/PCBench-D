    def _get_baseline(self, filename):
        if rcParams['text.latex.preview']:
            base, ext = os.path.splitext(filename)
            baseline_filename = base + ".baseline"
            if os.path.exists(baseline_filename):
                with open(baseline_filename, 'rb') as fd:
                    l = fd.read().split()
                height, depth, width = l
                return float(depth)
        return None
