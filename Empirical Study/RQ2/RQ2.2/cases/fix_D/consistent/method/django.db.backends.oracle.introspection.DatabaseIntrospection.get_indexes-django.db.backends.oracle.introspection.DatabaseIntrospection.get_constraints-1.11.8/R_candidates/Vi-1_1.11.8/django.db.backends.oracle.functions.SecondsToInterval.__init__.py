    def __init__(self, expression, **extra):
        output_field = extra.pop('output_field', DurationField())
        super(SecondsToInterval, self).__init__(expression, output_field=output_field, **extra)
