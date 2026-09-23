    def __init__(self, parent=None, parent_pos=(0, 0),
                 parent_inner=False, name='', ncols=1, nrows=1,
                 h_pad=None, w_pad=None, width_ratios=None,
                 height_ratios=None):
        Variable = kiwi.Variable
        self.parent = parent
        self.parent_pos = parent_pos
        self.parent_inner = parent_inner
        self.name = name + seq_id()
        if parent is not None:
            self.name = f'{parent.name}.{self.name}'
        self.nrows = nrows
        self.ncols = ncols
        self.height_ratios = np.atleast_1d(height_ratios)
        if height_ratios is None:
            self.height_ratios = np.ones(nrows)
        self.width_ratios = np.atleast_1d(width_ratios)
        if width_ratios is None:
            self.width_ratios = np.ones(ncols)

        sn = self.name + '_'
        if parent is None:
            self.parent = None
            self.solver = kiwi.Solver()
        else:
            self.parent = parent
            parent.add_child(self, *parent_pos)
            self.solver = self.parent.solver
        # keep track of artist associated w/ this layout.  Can be none
        self.artists = np.empty((nrows, ncols), dtype=object)
        self.children = np.empty((nrows, ncols), dtype=object)

        self.margins = {}
        self.margin_vals = {}
        # all the boxes in each column share the same left/right margins:
        for todo in ['left', 'right', 'leftcb', 'rightcb']:
            # track the value so we can change only if a margin is larger
            # than the current value
            self.margin_vals[todo] = np.zeros(ncols)

        sol = self.solver

        # These are redundant, but make life easier if
        # we define them all.  All that is really
        # needed is left/right, margin['left'], and margin['right']
        self.widths = [Variable(f'{sn}widths[{i}]') for i in range(ncols)]
        self.lefts = [Variable(f'{sn}lefts[{i}]') for i in range(ncols)]
        self.rights = [Variable(f'{sn}rights[{i}]') for i in range(ncols)]
        self.inner_widths = [Variable(f'{sn}inner_widths[{i}]')
                             for i in range(ncols)]
        for todo in ['left', 'right', 'leftcb', 'rightcb']:
            self.margins[todo] = [Variable(f'{sn}margins[{todo}][{i}]')
                                  for i in range(ncols)]
            for i in range(ncols):
                sol.addEditVariable(self.margins[todo][i], 'strong')

        for todo in ['bottom', 'top', 'bottomcb', 'topcb']:
            self.margins[todo] = np.empty((nrows), dtype=object)
            self.margin_vals[todo] = np.zeros(nrows)

        self.heights = [Variable(f'{sn}heights[{i}]') for i in range(nrows)]
        self.inner_heights = [Variable(f'{sn}inner_heights[{i}]')
                              for i in range(nrows)]
        self.bottoms = [Variable(f'{sn}bottoms[{i}]') for i in range(nrows)]
        self.tops = [Variable(f'{sn}tops[{i}]') for i in range(nrows)]
        for todo in ['bottom', 'top', 'bottomcb', 'topcb']:
            self.margins[todo] = [Variable(f'{sn}margins[{todo}][{i}]')
                                  for i in range(nrows)]
            for i in range(nrows):
                sol.addEditVariable(self.margins[todo][i], 'strong')

        # set these margins to zero by default. They will be edited as
        # children are filled.
        self.reset_margins()
        self.add_constraints()

        self.h_pad = h_pad
        self.w_pad = w_pad
