    def _populate_sub_fields(self, class_validators):
        # typing interface is horrible, we have to do some ugly checks
        origin = _get_type_origin(self.type_)
        if origin is None:
            # field is not "typing" object eg. Union, Dict, List etc.
            return

        if origin is Union:
            types_ = []
            for type_ in self.type_.__args__:
                if type_ is NoneType:
                    self.allow_none = True
                else:
                    types_.append(type_)
            self.sub_fields = [self.__class__(
                type_=t,
                class_validators=class_validators,
                default=self.default,
                required=self.required,
                allow_none=self.allow_none,
                name=f'{self.name}_{type_display(t)}',
                model_config=self.model_config,
            ) for t in types_]
        elif issubclass(origin, List):
            self.type_ = self.type_.__args__[0]
            self.shape = Shape.LIST
        elif issubclass(origin, Set):
            self.type_ = self.type_.__args__[0]
            self.shape = Shape.SET
        else:
            assert issubclass(origin, Mapping)
            self.key_type_ = self.type_.__args__[0]
            self.type_ = self.type_.__args__[1]
            self.shape = Shape.MAPPING
            self.key_field = self.__class__(
                type_=self.key_type_,
                class_validators=class_validators,
                default=self.default,
                required=self.required,
                allow_none=self.allow_none,
                name=f'key_{self.name}',
                model_config=self.model_config,
            )

        if not self.sub_fields and _get_type_origin(self.type_):
            # type_ has been refined eg. as the type of a List and sub_fields needs to be populated
            self.sub_fields = [self.__class__(
                type_=self.type_,
                class_validators=class_validators,
                default=self.default,
                required=self.required,
                allow_none=self.allow_none,
                name=f'_{self.name}',
                model_config=self.model_config,
            )]
