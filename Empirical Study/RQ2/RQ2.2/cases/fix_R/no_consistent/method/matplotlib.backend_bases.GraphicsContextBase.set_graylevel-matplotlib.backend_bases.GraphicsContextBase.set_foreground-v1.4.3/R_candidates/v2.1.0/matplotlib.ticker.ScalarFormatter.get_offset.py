    def get_offset(self):
        """
        Return scientific notation, plus offset.
        """
        if len(self.locs) == 0:
            return ''
        s = ''
        if self.orderOfMagnitude or self.offset:
            offsetStr = ''
            sciNotStr = ''
            if self.offset:
                offsetStr = self.format_data(self.offset)
                if self.offset > 0:
                    offsetStr = '+' + offsetStr
            if self.orderOfMagnitude:
                if self._usetex or self._useMathText:
                    sciNotStr = self.format_data(10 ** self.orderOfMagnitude)
                else:
                    sciNotStr = '1e%d' % self.orderOfMagnitude
            if self._useMathText:
                if sciNotStr != '':
                    sciNotStr = r'\times%s' % _mathdefault(sciNotStr)
                s = ''.join(('$', sciNotStr, _mathdefault(offsetStr), '$'))
            elif self._usetex:
                if sciNotStr != '':
                    sciNotStr = r'\times%s' % sciNotStr
                s = ''.join(('$', sciNotStr, offsetStr, '$'))
            else:
                s = ''.join((sciNotStr, offsetStr))

        return self.fix_minus(s)
