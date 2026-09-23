def test_rrulewrapper():
    def attach_tz(dt, zi):
        return dt.replace(tzinfo=zi)

    _test_rrulewrapper(attach_tz, dateutil.tz.gettz)
