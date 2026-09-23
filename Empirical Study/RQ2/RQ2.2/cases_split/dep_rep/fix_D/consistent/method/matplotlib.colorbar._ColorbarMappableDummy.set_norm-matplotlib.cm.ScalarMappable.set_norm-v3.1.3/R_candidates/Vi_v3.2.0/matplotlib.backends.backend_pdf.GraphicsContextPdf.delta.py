    def delta(self, other):
        """
        Copy properties of other into self and return PDF commands
        needed to transform self into other.
        """
        cmds = []
        fill_performed = False
        for params, cmd in self.commands:
            different = False
            for p in params:
                ours = getattr(self, p)
                theirs = getattr(other, p)
                try:
                    if ours is None or theirs is None:
                        different = ours is not theirs
                    else:
                        different = bool(ours != theirs)
                except ValueError:
                    ours = np.asarray(ours)
                    theirs = np.asarray(theirs)
                    different = (ours.shape != theirs.shape or
                                 np.any(ours != theirs))
                if different:
                    break

            # Need to update hatching if we also updated fillcolor
            if params == ('_hatch', '_hatch_color') and fill_performed:
                different = True

            if different:
                if params == ('_fillcolor',):
                    fill_performed = True
                theirs = [getattr(other, p) for p in params]
                cmds.extend(cmd(self, *theirs))
                for p in params:
                    setattr(self, p, getattr(other, p))
        return cmds
