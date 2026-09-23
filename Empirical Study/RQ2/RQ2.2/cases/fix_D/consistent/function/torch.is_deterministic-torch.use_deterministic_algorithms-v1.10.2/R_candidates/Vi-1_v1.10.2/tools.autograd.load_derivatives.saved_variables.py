def saved_variables(
    formula: str,
    nctypes: List[NamedCType],
    var_names: Tuple[str, ...],
) -> Tuple[str, Tuple[SavedAttribute, ...]]:

    def stride_expr(name: str) -> str:
        assert var_names == (name,), (
            'Replacement for ".strides()" is currently only supported for single derivatives of the same tensor '
            'that ".strides()" is being called on.')
        return f'strides_or_error({name}, "{name}")'

    REPLACEMENTS: List[Tuple[str, Dict[str, Any]]] = [
        # replace self.sizes() with self_sizes
        (r'{}.sizes\(\)', {
            'suffix': '_sizes',
            'nctype': lambda name: NamedCType(name, BaseCType(intArrayRefT)),
        }),
        # replace self.options() with self_options
        (r'{}.options\(\)', {
            'suffix': '_options',
            'nctype': lambda name: NamedCType(name, BaseCType(tensorOptionsT)),
        }),
        # replace zeros_like(self) with self_info
        (r'zeros_like\({}\)', {
            'suffix': '_info',
            'nctype': lambda name: NamedCType(name, BaseCType(typeAndSizeT)),
            'expr': lambda name: name,  # at save-time
            'res': lambda name: name + '_info.zeros()',  # at eval-time
        }),
        # replace self.size(2) with self_size_2
        (r'{}.size\((\w+)\)', {
            'suffix': lambda m: '_argsize_{}'.format(*m.groups()),
            'nctype': lambda name: NamedCType(name, BaseCType(intT)),
        }),
        # replace self.numel() with self_numel
        (r'{}.numel\(\)', {
            'suffix': '_numel',
            'nctype': lambda name: NamedCType(name, BaseCType(intT)),
        }),
        # replace to_args_sizes(self) with self_args_sizes
        (r'to_args_sizes\({}\)', {
            'suffix': '_args_sizes',
            'nctype': lambda name: NamedCType(name, VectorCType(VectorCType(BaseCType(intT)))),
        }),
        # replace to_args_scalartypes(self) with self_args_scalartypes
        (r'to_args_scalartypes\({}\)', {
            'suffix': '_args_scalartypes',
            'nctype': lambda name: NamedCType(name, VectorCType(BaseCType(scalarTypeT))),
        }),
        # replace TensorGeometry(self) with self_geometry
        (r'TensorGeometry\({}\)', {
            'suffix': '_geometry',
            'nctype': lambda name: NamedCType(name, BaseCType(tensorGeometryT)),
        }),
        (r'{}.scalar_type\(\)', {
            'suffix': '_scalar_type',
            'nctype': lambda name: NamedCType(name, BaseCType(scalarTypeT)),
        }),
        # replace self.dim() with self_dim
        (r'{}.dim\(\)', {
            'suffix': '_dim',
            'nctype': lambda name: NamedCType(name, BaseCType(intT)),
        }),
        # replace self.strides() with self_strides
        (r'{}.strides\(\)', {
            'suffix': '_strides',
            'nctype': lambda name: NamedCType(name, BaseCType(intArrayRefT)),
            'expr': stride_expr,
        }),
        # replace self.is_conj() with self_conjugate
        (r'{}.is_conj\(\)', {
            'suffix': '_conjugate',
            'nctype': lambda name: NamedCType(name, BaseCType(boolT)),
        })
    ]

    # find which arguments need to be saved
    saved: List[SavedAttribute] = []

    for nctype in nctypes:
        name = nctype.name.name if isinstance(nctype.name, SpecialArgName) else nctype.name
        # First search the formula for expressions which can be evaluated
        # when the autograd Function is created to avoid saving variables
        for regex, info in REPLACEMENTS:
            def repl(m: Match[str]) -> str:
                suffix: str = info['suffix'](m) if callable(info['suffix']) else info['suffix']
                expr: str = info['expr'](name) if 'expr' in info else m.group(0)
                saved.append(SavedAttribute(
                    nctype=info['nctype'](name + suffix),
                    expr=expr,
                ))
                if 'res' in info:
                    replacement: str = info['res'](name)
                    return replacement
                return name + suffix

            formula = re.sub(regex.format(name), repl, formula)

        # c10::optional<std::string> types stored in Backward nodes must be
        # converted to c10::optional<c10::string_view> before being passed into
        # the backward function
        if nctype.type == OptionalCType(BaseCType(stringT)):
            formula = re.sub(
                rf'\b{name}\b',
                f'{name}.has_value() ? c10::optional<c10::string_view>({name}.value()) : c10::nullopt',
                formula)

        # Find any variables which remain in the formula and save them
        if re.search(IDENT_REGEX.format(name), formula):
            saved.append(SavedAttribute(
                nctype=nctype,
                expr=name,
            ))

    return formula, tuple(saved)
