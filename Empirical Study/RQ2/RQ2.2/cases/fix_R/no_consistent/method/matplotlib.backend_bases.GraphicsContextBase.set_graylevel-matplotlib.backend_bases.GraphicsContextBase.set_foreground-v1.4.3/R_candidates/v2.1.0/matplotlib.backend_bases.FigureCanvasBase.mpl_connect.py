    def mpl_connect(self, s, func):
        """
        Connect event with string *s* to *func*.  The signature of *func* is::

          def func(event)

        where event is a :class:`matplotlib.backend_bases.Event`.  The
        following events are recognized

        - 'button_press_event'
        - 'button_release_event'
        - 'draw_event'
        - 'key_press_event'
        - 'key_release_event'
        - 'motion_notify_event'
        - 'pick_event'
        - 'resize_event'
        - 'scroll_event'
        - 'figure_enter_event',
        - 'figure_leave_event',
        - 'axes_enter_event',
        - 'axes_leave_event'
        - 'close_event'

        For the location events (button and key press/release), if the
        mouse is over the axes, the variable ``event.inaxes`` will be
        set to the :class:`~matplotlib.axes.Axes` the event occurs is
        over, and additionally, the variables ``event.xdata`` and
        ``event.ydata`` will be defined.  This is the mouse location
        in data coords.  See
        :class:`~matplotlib.backend_bases.KeyEvent` and
        :class:`~matplotlib.backend_bases.MouseEvent` for more info.

        Return value is a connection id that can be used with
        :meth:`~matplotlib.backend_bases.Event.mpl_disconnect`.

        Examples
        --------
        Usage::

            def on_press(event):
                print('you pressed', event.button, event.xdata, event.ydata)

            cid = canvas.mpl_connect('button_press_event', on_press)

        """
        if s == 'idle_event':
            warn_deprecated(1.5,
                "idle_event is only implemented for the wx backend, and will "
                "be removed in matplotlib 2.1. Use the animations module "
                "instead.")

        return self.callbacks.connect(s, func)
