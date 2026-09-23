    def __setattr__(self, name, value):
        if not self.__config__.allow_extra and name not in self.__fields__:
            raise ValueError(f'"{self.__class__.__name__}" object has no field "{name}"')
        elif not self.__config__.allow_mutation:
            raise TypeError(f'"{self.__class__.__name__}" is immutable and does not support item assignment')
        elif self.__config__.validate_assignment:
            value_, error_ = self.fields[name].validate(value, self.dict(exclude={name}))
            if error_:
                raise ValidationError({name: error_})
            else:
                self.__values__[name] = value_
        else:
            self.__values__[name] = value
