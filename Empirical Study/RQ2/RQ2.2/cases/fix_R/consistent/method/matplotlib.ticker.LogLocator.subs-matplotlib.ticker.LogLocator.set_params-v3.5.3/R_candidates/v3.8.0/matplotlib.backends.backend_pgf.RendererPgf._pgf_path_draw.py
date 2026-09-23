    def _pgf_path_draw(self, stroke=True, fill=False):
        actions = []
        if stroke:
            actions.append("stroke")
        if fill:
            actions.append("fill")
        _writeln(self.fh, r"\pgfusepath{%s}" % ",".join(actions))
