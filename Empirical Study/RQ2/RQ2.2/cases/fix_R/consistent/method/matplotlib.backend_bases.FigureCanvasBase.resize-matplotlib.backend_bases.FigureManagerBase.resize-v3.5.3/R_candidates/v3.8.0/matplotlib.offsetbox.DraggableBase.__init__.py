    def __init__(self, ref_artist, use_blit=False):
        self.ref_artist = ref_artist
        if not ref_artist.pickable():
            ref_artist.set_picker(True)
        self.got_artist = False
        self._use_blit = use_blit and self.canvas.supports_blit
        callbacks = ref_artist.figure._canvas_callbacks
        self._disconnectors = [
            functools.partial(
                callbacks.disconnect, callbacks._connect_picklable(name, func))
            for name, func in [
                ("pick_event", self.on_pick),
                ("button_release_event", self.on_release),
                ("motion_notify_event", self.on_motion),
            ]
        ]
