    def get_xaxis_transform(self, which='grid'):
        cbook._check_in_list(['tick1', 'tick2', 'grid'], which=which)
        return self._xaxis_transform
