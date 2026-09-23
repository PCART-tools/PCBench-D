def group_overloads(
    overloads: Sequence[PythonSignatureNativeFunctionPair],
) -> Sequence[PythonSignatureGroup]:
    bases: Dict[str, PythonSignatureNativeFunctionPair] = {}
    outplaces: Dict[str, PythonSignatureNativeFunctionPair] = {}

    # first group by signature ignoring out arguments
    for overload in overloads:
        sig = overload.signature.signature_str(skip_outputs=True)
        if overload.function.func.is_out_fn():
            if sig in outplaces:
                raise RuntimeError(
                    f'Found duplicated function definition:\n- {overload.function.func}.\n'
                    f'Existing definition:\n- {outplaces[sig].function.func}.'
                )
            outplaces[sig] = overload
        else:
            if sig in bases:
                raise RuntimeError(
                    f'Found duplicated function definition:\n- {overload.function.func}.\n'
                    f'Existing definition:\n- {bases[sig].function.func}.'
                )
            bases[sig] = overload

    for sig, out in outplaces.items():
        if sig not in bases:
            candidates: List[str] = []
            for overload in overloads:
                if str(overload.function.func.name.name) == str(out.function.func.name.name) \
                        and not overload.function.func.is_out_fn() \
                        and not overload.signature.deprecated:
                    candidates.append(overload.signature.signature_str(skip_outputs=True))
            out_sig = out.signature.signature_str()
            raise RuntimeError(
                f'While identifying overloads, we found an out schema {out_sig} without a corresponding non-out variant. '
                f'We expected the non-out variant to have schema: \n- {sig}\nPlease check that you spelled the schema '
                'correctly in native_functions.yaml. We discovered the following candidate(s): \n'
                + '\n'.join(f'- {candidate}' for candidate in candidates))

    grouped: List[PythonSignatureGroup] = []
    for sig, base in bases.items():
        outplace = outplaces.get(sig)
        grouped.append(PythonSignatureGroup(
            # prefer the signature with optional out=... arguments because it's the
            # superset that can be used to parse input for both base and outplace.
            signature=outplace.signature if outplace is not None else base.signature,
            base=base.function,
            outplace=outplace.function if outplace is not None else None,
        ))

    return sort_overloads(grouped)
