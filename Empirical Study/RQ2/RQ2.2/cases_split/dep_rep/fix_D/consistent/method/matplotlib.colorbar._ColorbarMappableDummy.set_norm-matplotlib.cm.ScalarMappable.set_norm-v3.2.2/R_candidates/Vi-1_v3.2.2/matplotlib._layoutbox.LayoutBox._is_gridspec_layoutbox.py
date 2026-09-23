    def _is_gridspec_layoutbox(self):
        '''
        Helper to check if this layoutbox is the layoutbox of a
        gridspec
        '''
        name = (self.name).split('.')[-1]
        return name[:8] == 'gridspec'
