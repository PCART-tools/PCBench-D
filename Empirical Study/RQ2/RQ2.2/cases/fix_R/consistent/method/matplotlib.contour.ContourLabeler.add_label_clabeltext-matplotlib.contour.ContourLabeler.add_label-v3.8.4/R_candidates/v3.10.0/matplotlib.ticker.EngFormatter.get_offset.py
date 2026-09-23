    def get_offset(self):
        # docstring inherited
        if len(self.locs) == 0:
            return ''
        if self.offset:
            offsetStr = ''
            if self.offset:
                offsetStr = self.format_data(self.offset)
                if self.offset > 0:
                    offsetStr = '+' + offsetStr
            sciNotStr = self.format_data(10 ** self.orderOfMagnitude)
            if self._useMathText or self._usetex:
                if sciNotStr != '':
                    sciNotStr = r'\times%s' % sciNotStr
                s = f'${sciNotStr}{offsetStr}$'
            else:
                s = sciNotStr + offsetStr
            return self.fix_minus(s)
        return ''
