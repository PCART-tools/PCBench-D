    def set(self, **kwargs):
        """A property batch setter.  Pass *kwargs* to set properties."""
        kwargs = cbook.normalize_kwargs(kwargs, self)
        move_color_to_start = False
        if "color" in kwargs:
            keys = [*kwargs]
            i_color = keys.index("color")
            props = ["edgecolor", "facecolor"]
            if any(tp.__module__ == "matplotlib.collections"
                   and tp.__name__ == "Collection"
                   for tp in type(self).__mro__):
                props.append("alpha")
            for other in props:
                if other not in keys:
                    continue
                i_other = keys.index(other)
                if i_other < i_color:
                    move_color_to_start = True
                    _api.warn_deprecated(
                        "3.3", message=f"You have passed the {other!r} kwarg "
                        "before the 'color' kwarg.  Artist.set() currently "
                        "reorders the properties to apply 'color' first, but "
                        "this is deprecated since %(since)s and will be "
                        "removed %(removal)s; please pass 'color' first "
                        "instead.")
        if move_color_to_start:
            kwargs = {"color": kwargs.pop("color"), **kwargs}
        return self.update(kwargs)
