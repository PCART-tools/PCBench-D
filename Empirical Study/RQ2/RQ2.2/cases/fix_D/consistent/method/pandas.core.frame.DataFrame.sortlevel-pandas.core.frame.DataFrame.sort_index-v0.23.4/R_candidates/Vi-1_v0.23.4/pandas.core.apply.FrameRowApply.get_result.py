    def get_result(self):

        # dispatch to agg
        if isinstance(self.f, (list, dict)):
            return self.obj.aggregate(self.f, axis=self.axis,
                                      *self.args, **self.kwds)

        return super(FrameRowApply, self).get_result()
