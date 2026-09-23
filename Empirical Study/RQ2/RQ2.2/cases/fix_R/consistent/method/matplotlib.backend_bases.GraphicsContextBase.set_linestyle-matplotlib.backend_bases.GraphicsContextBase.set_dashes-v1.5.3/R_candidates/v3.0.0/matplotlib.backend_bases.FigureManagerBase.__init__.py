    def __init__(self, canvas, num):
        self.canvas = canvas
        canvas.manager = self  # store a pointer to parent
        self.num = num

        self.key_press_handler_id = None
        if rcParams['toolbar'] != 'toolmanager':
            self.key_press_handler_id = self.canvas.mpl_connect(
                'key_press_event',
                self.key_press)

        self.toolmanager = None
        self.toolbar = None

        @self.canvas.figure.add_axobserver
        def notify_axes_change(fig):
            # Called whenever the current axes is changed.
            if self.toolmanager is None and self.toolbar is not None:
                self.toolbar.update()
