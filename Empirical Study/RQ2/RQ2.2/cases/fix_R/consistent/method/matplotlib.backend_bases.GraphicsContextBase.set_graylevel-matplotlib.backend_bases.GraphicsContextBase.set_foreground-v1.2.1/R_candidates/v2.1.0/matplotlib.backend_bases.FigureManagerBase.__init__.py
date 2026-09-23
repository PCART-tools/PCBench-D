    def __init__(self, canvas, num):
        self.canvas = canvas
        canvas.manager = self  # store a pointer to parent
        self.num = num

        self.key_press_handler_id = None
        """
        The returned id from connecting the default key handler via
        :meth:`FigureCanvasBase.mpl_connect`.

        To disable default key press handling::

            manager, canvas = figure.canvas.manager, figure.canvas
            canvas.mpl_disconnect(manager.key_press_handler_id)

        """
        if rcParams['toolbar'] != 'toolmanager':
            self.key_press_handler_id = self.canvas.mpl_connect(
                'key_press_event',
                self.key_press)
