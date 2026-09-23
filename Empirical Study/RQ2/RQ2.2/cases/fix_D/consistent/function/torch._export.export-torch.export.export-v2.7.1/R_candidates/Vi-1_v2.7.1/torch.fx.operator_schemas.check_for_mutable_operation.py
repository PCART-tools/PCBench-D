@compatibility(is_backward_compatible=False)
def check_for_mutable_operation(
    target: Callable, args: tuple["Argument", ...], kwargs: dict[str, "Argument"]
):
    signatures, schemas = get_signature_for_torch_op(target, return_schemas=True)

    if signatures and schemas:
        matched_schemas = []

        # Iterate through all of the schema until we find one that matches
        # If one matches, populate `new_args_and_kwargs` with the new args/kwargs
        # values. If none matches, `new_args_and_kwargs` will be None
        for candidate_signature, schema in zip(signatures, schemas):
            try:
                candidate_signature.bind(*args, **kwargs)
                matched_schemas.append((candidate_signature, schema))
            except TypeError:
                continue

        def throw_if_mutable(schema):
            if schema.is_mutable:
                raise RuntimeError(
                    f"Tried to trace mutable operation {schema}. FX only supports functional "
                    f"code, so operations that mutate operands in-place (e.g. via `out` arguments) "
                    f"are not supported"
                )

        if len(matched_schemas) == 0:
            # Did not match any schema. Cannot check for mutation
            pass
        elif len(matched_schemas) == 1:
            # Matched exactly one schema, unambiguous
            _, schema_to_check = matched_schemas[0]
            throw_if_mutable(schema_to_check)
        else:
            # Ambiguous schema match. Since mutability checking is best effort,
            # do nothing.
            pass
