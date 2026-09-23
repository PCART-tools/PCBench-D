    def to_object_block(self, mgr):
        """
        return myself as an object block

        Since we keep the DTI as a 1-d object, this is different
        depends on BlockManager's ndim
        """
        values = self.get_values(dtype=object)
        kwargs = {}
        if mgr.ndim > 1:
            values = _block_shape(values, ndim=mgr.ndim)
            kwargs['ndim'] = mgr.ndim
            kwargs['placement'] = [0]
        return self.make_block(values, klass=ObjectBlock, **kwargs)
