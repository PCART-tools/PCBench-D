    @staticmethod
    def _translate_tick_kw(kw, to_init_kw=True):
        # The following lists may be moved to a more
        # accessible location.
        kwkeys0 = ['size', 'width', 'color', 'tickdir', 'pad',
                   'labelsize', 'labelcolor', 'zorder', 'gridOn',
                   'tick1On', 'tick2On', 'label1On', 'label2On']
        kwkeys1 = ['length', 'direction', 'left', 'bottom', 'right', 'top',
                   'labelleft', 'labelbottom', 'labelright', 'labeltop',
                   'labelrotation']
        kwkeys2 = _gridline_param_names
        kwkeys = kwkeys0 + kwkeys1 + kwkeys2
        kwtrans = dict()
        if to_init_kw:
            if 'length' in kw:
                kwtrans['size'] = kw.pop('length')
            if 'direction' in kw:
                kwtrans['tickdir'] = kw.pop('direction')
            if 'rotation' in kw:
                kwtrans['labelrotation'] = kw.pop('rotation')
            if 'left' in kw:
                kwtrans['tick1On'] = _string_to_bool(kw.pop('left'))
            if 'bottom' in kw:
                kwtrans['tick1On'] = _string_to_bool(kw.pop('bottom'))
            if 'right' in kw:
                kwtrans['tick2On'] = _string_to_bool(kw.pop('right'))
            if 'top' in kw:
                kwtrans['tick2On'] = _string_to_bool(kw.pop('top'))

            if 'labelleft' in kw:
                kwtrans['label1On'] = _string_to_bool(kw.pop('labelleft'))
            if 'labelbottom' in kw:
                kwtrans['label1On'] = _string_to_bool(kw.pop('labelbottom'))
            if 'labelright' in kw:
                kwtrans['label2On'] = _string_to_bool(kw.pop('labelright'))
            if 'labeltop' in kw:
                kwtrans['label2On'] = _string_to_bool(kw.pop('labeltop'))
            if 'colors' in kw:
                c = kw.pop('colors')
                kwtrans['color'] = c
                kwtrans['labelcolor'] = c
            # Maybe move the checking up to the caller of this method.
            for key in kw:
                if key not in kwkeys:
                    raise ValueError(
                        "keyword %s is not recognized; valid keywords are %s"
                        % (key, kwkeys))
            kwtrans.update(kw)
        else:
            raise NotImplementedError("Inverse translation is deferred")
        return kwtrans
