    def get_majorticklines(self):
        r"""Return this Axis' major tick lines as a list of `.Line2D`\s."""
        lines = []
        ticks = self.get_major_ticks()
        for tick in ticks:
            lines.append(tick.tick1line)
            lines.append(tick.tick2line)
        return cbook.silent_list('Line2D ticklines', lines)
