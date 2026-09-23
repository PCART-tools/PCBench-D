    @staticmethod
    def _mpl_modifiers(event_state, *, exclude=None):
        modifiers = [
            ("ctrl", Gdk.ModifierType.CONTROL_MASK, "control"),
            ("alt", Gdk.ModifierType.MOD1_MASK, "alt"),
            ("shift", Gdk.ModifierType.SHIFT_MASK, "shift"),
            ("super", Gdk.ModifierType.MOD4_MASK, "super"),
        ]
        return [name for name, mask, key in modifiers
                if exclude != key and event_state & mask]
