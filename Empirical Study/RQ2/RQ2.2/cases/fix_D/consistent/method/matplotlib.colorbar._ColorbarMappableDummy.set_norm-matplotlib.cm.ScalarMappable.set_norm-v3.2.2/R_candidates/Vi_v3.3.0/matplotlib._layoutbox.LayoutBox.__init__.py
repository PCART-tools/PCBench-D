    def __init__(self, parent=None, name='', tightwidth=False,
                 tightheight=False, artist=None,
                 lower_left=(0, 0), upper_right=(1, 1), pos=False,
                 subplot=False, h_pad=None, w_pad=None):
        Variable = kiwi.Variable
        self.parent = parent
        self.name = name
        sn = self.name + '_'
        if parent is None:
            self.solver = kiwi.Solver()
            self.constrained_layout_called = 0
        else:
            self.solver = parent.solver
            self.constrained_layout_called = None
            # parent wants to know about this child!
            parent.add_child(self)
        # keep track of artist associated w/ this layout.  Can be none
        self.artist = artist
        # keep track if this box is supposed to be a pos that is constrained
        # by the parent.
        self.pos = pos
        # keep track of whether we need to match this subplot up with others.
        self.subplot = subplot

        self.top = Variable(sn + 'top')
        self.bottom = Variable(sn + 'bottom')
        self.left = Variable(sn + 'left')
        self.right = Variable(sn + 'right')

        self.width = Variable(sn + 'width')
        self.height = Variable(sn + 'height')
        self.h_center = Variable(sn + 'h_center')
        self.v_center = Variable(sn + 'v_center')

        self.min_width = Variable(sn + 'min_width')
        self.min_height = Variable(sn + 'min_height')
        self.pref_width = Variable(sn + 'pref_width')
        self.pref_height = Variable(sn + 'pref_height')
        # margins are only used for axes-position layout boxes.  maybe should
        # be a separate subclass:
        self.left_margin = Variable(sn + 'left_margin')
        self.right_margin = Variable(sn + 'right_margin')
        self.bottom_margin = Variable(sn + 'bottom_margin')
        self.top_margin = Variable(sn + 'top_margin')
        # mins
        self.left_margin_min = Variable(sn + 'left_margin_min')
        self.right_margin_min = Variable(sn + 'right_margin_min')
        self.bottom_margin_min = Variable(sn + 'bottom_margin_min')
        self.top_margin_min = Variable(sn + 'top_margin_min')

        right, top = upper_right
        left, bottom = lower_left
        self.tightheight = tightheight
        self.tightwidth = tightwidth
        self.add_constraints()
        self.children = []
        self.subplotspec = None
        if self.pos:
            self.constrain_margins()
        self.h_pad = h_pad
        self.w_pad = w_pad
