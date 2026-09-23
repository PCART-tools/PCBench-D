    def __unicode__(self):
        # currently, unicode is same as repr...fixes infinite loop
        series_rep = Series.__unicode__(self)
        rep = '%s\n%s' % (series_rep, repr(self.sp_index))
        return rep
