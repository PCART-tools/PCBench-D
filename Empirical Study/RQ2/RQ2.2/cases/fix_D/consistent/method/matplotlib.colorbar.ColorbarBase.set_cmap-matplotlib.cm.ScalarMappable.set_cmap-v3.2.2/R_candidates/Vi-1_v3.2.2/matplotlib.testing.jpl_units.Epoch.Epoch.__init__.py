    def __init__(self, frame, sec=None, jd=None, daynum=None, dt=None):
        """Create a new Epoch object.

        Build an epoch 1 of 2 ways:

        Using seconds past a Julian date:
        #   Epoch('ET', sec=1e8, jd=2451545)

        or using a matplotlib day number
        #   Epoch('ET', daynum=730119.5)

        = ERROR CONDITIONS
        - If the input units are not in the allowed list, an error is thrown.

        = INPUT VARIABLES
        - frame     The frame of the epoch.  Must be 'ET' or 'UTC'
        - sec        The number of seconds past the input JD.
        - jd         The Julian date of the epoch.
        - daynum    The matplotlib day number of the epoch.
        - dt         A python datetime instance.
        """
        if ((sec is None and jd is not None) or
                (sec is not None and jd is None) or
                (daynum is not None and
                 (sec is not None or jd is not None)) or
                (daynum is None and dt is None and
                 (sec is None or jd is None)) or
                (daynum is not None and dt is not None) or
                (dt is not None and (sec is not None or jd is not None)) or
                ((dt is not None) and not isinstance(dt, DT.datetime))):
            raise ValueError(
                "Invalid inputs.  Must enter sec and jd together, "
                "daynum by itself, or dt (must be a python datetime).\n"
                "Sec = %s\n"
                "JD  = %s\n"
                "dnum= %s\n"
                "dt  = %s" % (sec, jd, daynum, dt))

        cbook._check_in_list(self.allowed, frame=frame)
        self._frame = frame

        if dt is not None:
            daynum = date2num(dt)

        if daynum is not None:
            # 1-JAN-0001 in JD = 1721425.5
            jd = float(daynum) + 1721425.5
            self._jd = math.floor(jd)
            self._seconds = (jd - self._jd) * 86400.0

        else:
            self._seconds = float(sec)
            self._jd = float(jd)

            # Resolve seconds down to [ 0, 86400)
            deltaDays = math.floor(self._seconds / 86400)
            self._jd += deltaDays
            self._seconds -= deltaDays * 86400.0
