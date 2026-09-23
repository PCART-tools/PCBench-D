    def get_yaxis_transform(self,which='grid'):
        if which not in ['tick1','tick2','grid']:
            msg = "'which' must be one of [ 'tick1' | 'tick2' | 'grid' ]"
            raise ValueError(msg)
        return self._yaxis_transform
