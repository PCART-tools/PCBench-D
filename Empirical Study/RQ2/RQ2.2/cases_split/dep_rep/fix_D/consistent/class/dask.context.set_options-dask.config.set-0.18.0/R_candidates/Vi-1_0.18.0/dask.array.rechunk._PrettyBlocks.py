class _PrettyBlocks(object):

    def __init__(self, blocks):
        self.blocks = blocks

    def __str__(self):
        runs = []
        run = []
        repeats = 0
        for c in self.blocks:
            if run and run[-1] == c:
                if repeats == 0 and len(run) > 1:
                    runs.append((None, run[:-1]))
                    run = run[-1:]
                repeats += 1
            else:
                if repeats > 0:
                    assert len(run) == 1
                    runs.append((repeats + 1, run[-1]))
                    run = []
                    repeats = 0
                run.append(c)
        if run:
            if repeats == 0:
                runs.append((None, run))
            else:
                assert len(run) == 1
                runs.append((repeats + 1, run[-1]))

        parts = []
        for repeats, run in runs:
            if repeats is None:
                parts.append(str(run))
            else:
                parts.append("%d*[%s]" % (repeats, run))
        return " | ".join(parts)

    __repr__ = __str__
