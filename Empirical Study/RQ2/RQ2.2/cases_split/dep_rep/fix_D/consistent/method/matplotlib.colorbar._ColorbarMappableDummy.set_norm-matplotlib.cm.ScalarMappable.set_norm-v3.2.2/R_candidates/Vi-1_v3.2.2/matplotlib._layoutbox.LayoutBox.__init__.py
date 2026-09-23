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

        # we need the str below for Py 2 which complains the string is unicode
        self.top = Variable(str(sn + 'top'))
        self.bottom = Variable(str(sn + 'bottom'))
        self.left = Variable(str(sn + 'left'))
        self.right = Variable(str(sn + 'right'))

        self.width = Variable(str(sn + 'width'))
        self.height = Variable(str(sn + 'height'))
        self.h_center = Variable(str(sn + 'h_center'))
        self.v_center = Variable(str(sn + 'v_center'))

        self.min_width = Variable(str(sn + 'min_width'))
        self.min_height = Variable(str(sn + 'min_height'))
        self.pref_width = Variable(str(sn + 'pref_width'))
        self.pref_height = Variable(str(sn + 'pref_height'))
        # margins are only used for axes-position layout boxes.  maybe should
        # be a separate subclass:
        self.left_margin = Variable(str(sn + 'left_margin'))
        self.right_margin = Variable(str(sn + 'right_margin'))
        self.bottom_margin = Variable(str(sn + 'bottom_margin'))
        self.top_margin = Variable(str(sn + 'top_margin'))
        # mins
        self.left_margin_min = Variable(str(sn + 'left_margin_min'))
        self.right_margin_min = Variable(str(sn + 'right_margin_min'))
        self.bottom_margin_min = Variable(str(sn + 'bottom_margin_min'))
        self.top_margin_min = Variable(str(sn + 'top_margin_min'))

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
