    @staticmethod
    def _translate_tick_params(kw):
        """
        Translate the kwargs supported by `.Axis.set_tick_params` to kwargs
        supported by `.Tick._apply_params`.

        In particular, this maps axis specific names like 'top', 'left'
        to the generic tick1, tick2 logic of the axis. Additionally, there
        are some other name translations.

        Returns a new dict of translated kwargs.

        Note: The input *kwargs* are currently modified, but that's ok for
        the only caller.
        """
        # The following lists may be moved to a more accessible location.
        allowed_keys = [
            'size', 'width', 'color', 'tickdir', 'pad',
            'labelsize', 'labelcolor', 'zorder', 'gridOn',
            'tick1On', 'tick2On', 'label1On', 'label2On',
            'length', 'direction', 'left', 'bottom', 'right', 'top',
            'labelleft', 'labelbottom', 'labelright', 'labeltop',
            'labelrotation',
            *_gridline_param_names]

        keymap = {
            # tick_params key -> axis key
            'length': 'size',
            'direction': 'tickdir',
            'rotation': 'labelrotation',
            'left': 'tick1On',
            'bottom': 'tick1On',
            'right': 'tick2On',
            'top': 'tick2On',
            'labelleft': 'label1On',
            'labelbottom': 'label1On',
            'labelright': 'label2On',
            'labeltop': 'label2On',
        }
        kwtrans = {newkey: kw.pop(oldkey)
                   for oldkey, newkey in keymap.items() if oldkey in kw}
        if 'colors' in kw:
            c = kw.pop('colors')
            kwtrans['color'] = c
            kwtrans['labelcolor'] = c
        # Maybe move the checking up to the caller of this method.
        for key in kw:
            if key not in allowed_keys:
                raise ValueError(
                    "keyword %s is not recognized; valid keywords are %s"
                    % (key, allowed_keys))
        kwtrans.update(kw)
        return kwtrans
