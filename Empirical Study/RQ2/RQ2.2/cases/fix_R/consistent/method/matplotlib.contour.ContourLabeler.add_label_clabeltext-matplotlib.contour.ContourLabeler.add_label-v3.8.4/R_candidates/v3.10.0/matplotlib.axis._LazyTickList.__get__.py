    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            # instance._get_tick() can itself try to access the majorTicks
            # attribute (e.g. in certain projection classes which override
            # e.g. get_xaxis_text1_transform).  In order to avoid infinite
            # recursion, first set the majorTicks on the instance temporarily
            # to an empty lis. Then create the tick; note that _get_tick()
            # may call reset_ticks(). Therefore, the final tick list is
            # created and assigned afterwards.
            if self._major:
                instance.majorTicks = []
                tick = instance._get_tick(major=True)
                instance.majorTicks = [tick]
                return instance.majorTicks
            else:
                instance.minorTicks = []
                tick = instance._get_tick(major=False)
                instance.minorTicks = [tick]
                return instance.minorTicks
