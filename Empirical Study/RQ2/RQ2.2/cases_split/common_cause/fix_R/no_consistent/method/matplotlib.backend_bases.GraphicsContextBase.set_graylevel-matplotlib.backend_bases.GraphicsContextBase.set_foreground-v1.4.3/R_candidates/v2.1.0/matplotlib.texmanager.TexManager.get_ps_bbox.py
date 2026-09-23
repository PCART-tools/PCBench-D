    def get_ps_bbox(self, tex, fontsize):
        """
        returns a list containing the postscript bounding box for latex's
        rendering of the tex string
        """
        psfile = self.make_ps(tex, fontsize)
        with open(psfile) as ps:
            for line in ps:
                if line.startswith('%%BoundingBox:'):
                    return [int(val) for val in line.split()[1:]]
        raise RuntimeError('Could not parse %s' % psfile)
