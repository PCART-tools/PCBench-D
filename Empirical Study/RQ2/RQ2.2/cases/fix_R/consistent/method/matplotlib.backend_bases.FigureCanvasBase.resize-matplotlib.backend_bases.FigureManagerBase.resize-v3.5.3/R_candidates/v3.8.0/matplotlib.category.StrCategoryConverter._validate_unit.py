    @staticmethod
    def _validate_unit(unit):
        if not hasattr(unit, '_mapping'):
            raise ValueError(
                f'Provided unit "{unit}" is not valid for a categorical '
                'converter, as it does not have a _mapping attribute.')
