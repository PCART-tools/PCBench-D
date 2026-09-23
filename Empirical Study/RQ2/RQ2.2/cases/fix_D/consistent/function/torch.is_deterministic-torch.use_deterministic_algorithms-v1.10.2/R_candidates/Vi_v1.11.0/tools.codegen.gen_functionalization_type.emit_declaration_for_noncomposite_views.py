def emit_declaration_for_noncomposite_views(f: NativeFunction) -> str:
    # For every view op, we need a corresponding "inverse view" function.
    # This generates the declarations so we get a good compiler error when someone adds a new view.
    view_inverse_sig = ViewInverseSignature(f)
    return view_inverse_sig.decl()
