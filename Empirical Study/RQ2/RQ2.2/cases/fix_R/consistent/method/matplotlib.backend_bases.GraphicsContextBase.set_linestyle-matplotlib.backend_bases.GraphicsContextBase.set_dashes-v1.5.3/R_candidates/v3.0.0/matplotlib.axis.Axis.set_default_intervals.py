    def set_default_intervals(self):
        '''set the default limits for the axis data and view interval if they
        are not mutated'''

        # this is mainly in support of custom object plotting.  For
        # example, if someone passes in a datetime object, we do not
        # know automagically how to set the default min/max of the
        # data and view limits.  The unit conversion AxisInfo
        # interface provides a hook for custom types to register
        # default limits through the AxisInfo.default_limits
        # attribute, and the derived code below will check for that
        # and use it if is available (else just use 0..1)
        pass
