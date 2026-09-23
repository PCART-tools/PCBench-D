def argument(a: Argument, *, remove_non_owning_ref_types: bool = False) -> Binding:
    return Binding(
        nctype=argument_type(a, binds=a.name, remove_non_owning_ref_types=remove_non_owning_ref_types),
        name=a.name,
        argument=a
    )
