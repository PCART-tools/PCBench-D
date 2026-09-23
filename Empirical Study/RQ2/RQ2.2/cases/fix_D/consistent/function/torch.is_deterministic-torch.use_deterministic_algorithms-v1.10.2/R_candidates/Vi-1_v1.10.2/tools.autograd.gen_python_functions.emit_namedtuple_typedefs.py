def emit_namedtuple_typedefs(
    overloads: Sequence[PythonSignatureNativeFunctionPair]
) -> Tuple[List[str], Dict[str, str]]:
    """
    Generate block of named tuple type def inits, and add typeref snippets
    to declarations that use them
    """
    flddefnames: Dict[str, str] = {}  # map from unique field name lists to field def name
    flddefs: List[str] = []           # field def declarations
    typenames: Dict[str, str] = {}    # map from unique name + field name lists to typedef name
    typedefs: List[str] = []          # typedef declarations and init code

    for overload in overloads:
        fieldnames = namedtuple_fieldnames(overload.function.func.returns)
        if not fieldnames:
            continue

        fn_key = '_'.join(fieldnames)
        fieldsname = flddefnames.get(fn_key)
        if fieldsname is None:
            fieldsname = f'NamedTuple_fields{"" if not flddefs else len(flddefs)}'
            flddefnames[fn_key] = fieldsname
            fields = ', '.join(f'{{"{fn}", ""}}' for fn in fieldnames)
            flddefs.append(f"""\
static PyStructSequence_Field {fieldsname}[] = {{ {fields},  {{nullptr}} }};
""")

        name = cpp.name(overload.function.func)  # use @with_native_function?
        tn_key = gen_namedtuple_typename_key(overload.function)
        typename = typenames.get(tn_key)
        if typename is None:
            typename = f'NamedTuple{"" if not typedefs else len(typedefs)}'
            typenames[tn_key] = typename
            typedefs.append(f"""\
static PyTypeObject {typename};
static bool {typename}_initialized = false;
if (!{typename}_initialized) {{
  {typename}_initialized = true;
  static PyStructSequence_Desc desc = {{ "torch.return_types.{name}", nullptr, {fieldsname}, {len(fieldnames)} }};
  PyStructSequence_InitType(&{typename}, &desc);
  {typename}.tp_repr = (reprfunc)torch::utils::returned_structseq_repr;
}}
""")

    return flddefs + typedefs, typenames
