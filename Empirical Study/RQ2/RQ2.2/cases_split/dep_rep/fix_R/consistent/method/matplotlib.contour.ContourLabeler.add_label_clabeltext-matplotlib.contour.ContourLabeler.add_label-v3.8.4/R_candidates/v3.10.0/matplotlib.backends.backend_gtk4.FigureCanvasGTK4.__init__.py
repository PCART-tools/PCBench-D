    def __init__(self, figure=None):
        super().__init__(figure=figure)

        self.set_hexpand(True)
        self.set_vexpand(True)

        self._idle_draw_id = 0
        self._rubberband_rect = None

        self.set_draw_func(self._draw_func)
        self.connect('resize', self.resize_event)
        self.connect('notify::scale-factor', self._update_device_pixel_ratio)

        click = Gtk.GestureClick()
        click.set_button(0)  # All buttons.
        click.connect('pressed', self.button_press_event)
        click.connect('released', self.button_release_event)
        self.add_controller(click)

        key = Gtk.EventControllerKey()
        key.connect('key-pressed', self.key_press_event)
        key.connect('key-released', self.key_release_event)
        self.add_controller(key)

        motion = Gtk.EventControllerMotion()
        motion.connect('motion', self.motion_notify_event)
        motion.connect('enter', self.enter_notify_event)
        motion.connect('leave', self.leave_notify_event)
        self.add_controller(motion)

        scroll = Gtk.EventControllerScroll.new(
            Gtk.EventControllerScrollFlags.VERTICAL)
        scroll.connect('scroll', self.scroll_event)
        self.add_controller(scroll)

        self.set_focusable(True)

        css = Gtk.CssProvider()
        style = '.matplotlib-canvas { background-color: white; }'
        if Gtk.check_version(4, 9, 3) is None:
            css.load_from_data(style, -1)
        else:
            css.load_from_data(style.encode('utf-8'))
        style_ctx = self.get_style_context()
        style_ctx.add_provider(css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        style_ctx.add_class("matplotlib-canvas")
