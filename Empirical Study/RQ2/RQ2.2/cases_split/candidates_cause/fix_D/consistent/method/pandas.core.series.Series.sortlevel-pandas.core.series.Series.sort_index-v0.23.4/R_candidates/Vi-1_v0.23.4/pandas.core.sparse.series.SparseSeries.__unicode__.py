    def __unicode__(self):
        # currently, unicode is same as repr...fixes infinite loop
        series_rep = Series.__unicode__(self)
        rep = '{series}\n{index!r}'.format(series=series_rep,
                                           index=self.sp_index)
        return rep
