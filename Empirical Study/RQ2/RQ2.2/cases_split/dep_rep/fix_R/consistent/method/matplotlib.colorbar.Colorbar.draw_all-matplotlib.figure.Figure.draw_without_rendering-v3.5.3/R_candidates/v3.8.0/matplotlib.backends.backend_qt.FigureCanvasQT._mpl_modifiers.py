    @staticmethod
    def _mpl_modifiers(modifiers=None, *, exclude=None):
        if modifiers is None:
            modifiers = QtWidgets.QApplication.instance().keyboardModifiers()
        modifiers = _to_int(modifiers)
        # get names of the pressed modifier keys
        # 'control' is named 'control' when a standalone key, but 'ctrl' when a
        # modifier
        # bit twiddling to pick out modifier keys from modifiers bitmask,
        # if exclude is a MODIFIER, it should not be duplicated in mods
        return [SPECIAL_KEYS[key].replace('control', 'ctrl')
                for mask, key in _MODIFIER_KEYS
                if exclude != key and modifiers & mask]
