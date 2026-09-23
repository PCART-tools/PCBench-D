def _format_import_block(globals: Dict[str, Any], importer: Importer):
    import_strs: Set[str] = set()
    for name, obj in globals.items():
        import_strs.add(_format_import_statement(name, obj, importer))
    return '\n'.join(import_strs)
