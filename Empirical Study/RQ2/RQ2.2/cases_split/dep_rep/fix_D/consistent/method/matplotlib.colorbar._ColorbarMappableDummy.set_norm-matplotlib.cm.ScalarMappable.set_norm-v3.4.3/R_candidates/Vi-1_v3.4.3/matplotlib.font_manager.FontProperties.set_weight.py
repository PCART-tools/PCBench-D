    def set_weight(self, weight):
        """
        Set the font weight.  May be either a numeric value in the
        range 0-1000 or one of 'ultralight', 'light', 'normal',
        'regular', 'book', 'medium', 'roman', 'semibold', 'demibold',
        'demi', 'bold', 'heavy', 'extra bold', 'black'
        """
        if weight is None:
            weight = rcParams['font.weight']
        try:
            weight = int(weight)
            if weight < 0 or weight > 1000:
                raise ValueError()
        except ValueError:
            if weight not in weight_dict:
                raise ValueError("weight is invalid")
        self._weight = weight
