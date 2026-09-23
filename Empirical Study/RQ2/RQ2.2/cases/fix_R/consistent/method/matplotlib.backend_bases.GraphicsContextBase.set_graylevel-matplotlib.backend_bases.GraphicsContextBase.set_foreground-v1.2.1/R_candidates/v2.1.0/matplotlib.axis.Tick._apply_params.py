    def _apply_params(self, **kw):
        switchkw = ['gridOn', 'tick1On', 'tick2On', 'label1On', 'label2On']
        switches = [k for k in kw if k in switchkw]
        for k in switches:
            setattr(self, k, kw.pop(k))
        newmarker = [k for k in kw if k in ['size', 'width', 'pad', 'tickdir']]
        if newmarker:
            self._size = kw.pop('size', self._size)
            # Width could be handled outside this block, but it is
            # convenient to leave it here.
            self._width = kw.pop('width', self._width)
            self._base_pad = kw.pop('pad', self._base_pad)
            # apply_tickdir uses _size and _base_pad to make _pad,
            # and also makes _tickmarkers.
            self.apply_tickdir(kw.pop('tickdir', self._tickdir))
            self.tick1line.set_marker(self._tickmarkers[0])
            self.tick2line.set_marker(self._tickmarkers[1])
            for line in (self.tick1line, self.tick2line):
                line.set_markersize(self._size)
                line.set_markeredgewidth(self._width)
            # _get_text1_transform uses _pad from apply_tickdir.
            trans = self._get_text1_transform()[0]
            self.label1.set_transform(trans)
            trans = self._get_text2_transform()[0]
            self.label2.set_transform(trans)
        tick_kw = {k: v for k, v in six.iteritems(kw)
                   if k in ['color', 'zorder']}
        if tick_kw:
            self.tick1line.set(**tick_kw)
            self.tick2line.set(**tick_kw)
            for k, v in six.iteritems(tick_kw):
                setattr(self, '_' + k, v)

        if 'labelrotation' in kw:
            self._set_labelrotation(kw.pop('labelrotation'))
            self.label1.set(rotation=self._labelrotation[1])
            self.label2.set(rotation=self._labelrotation[1])

        label_list = [k for k in six.iteritems(kw)
                      if k[0] in ['labelsize', 'labelcolor']]
        if label_list:
            label_kw = {k[5:]: v for k, v in label_list}
            self.label1.set(**label_kw)
            self.label2.set(**label_kw)
            for k, v in six.iteritems(label_kw):
                # for labelsize the text objects covert str ('small')
                # -> points. grab the integer from the `Text` object
                # instead of saving the string representation
                v = getattr(self.label1, 'get_' + k)()
                setattr(self, '_label' + k, v)
