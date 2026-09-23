def gen_class(op, op_def):
    attributes = op_def["attributes"]
    attribute_args = []
    default_init = "NeuralNetOperator(NNKind::{op})".format(op=op)
    attribute_init = [default_init]
    attribute_declarations = []
    attribute_getters = []
    attribute_setters = []
    for attr in attributes:
        lower_name = attr[0][0].lower() + attr[0][1:]
        private_name = lower_name + "_"
        default_arg = "" if len(attr) < 3 else " = {}".format(attr[2])
        name = attr[0]
        t = attr[1]
        attr_arg = "{type} {lower_name}".format(
            type=t, lower_name=lower_name + default_arg
        )
        attr_init = "{private_name}({lower_name})".format(
            private_name=private_name, lower_name=lower_name)
        attr_declare = "{type} {private_name};".format(
            type=t, private_name=private_name)
        attr_get = dedent(
            """
              {type} get{name}() const {{
                return {private_name};
              }}
            """.format(
                type=t, name=name, private_name=private_name
            )
        )
        attr_set = dedent(
            """
              void set{name}({type} {lower_name}) {{
                {private_name} = {lower_name};
              }}
            """.format(
                type=t, name=name, private_name=private_name, lower_name=lower_name
            )
        )
        attribute_args.append(attr_arg)
        attribute_init.append(attr_init)
        attribute_declarations.append(attr_declare)
        attribute_getters.append(attr_get)
        attribute_setters.append(attr_set)

    extra_init = ""
    if "init_from" in op_def:
        for other_op in op_def["init_from"]:
            lower_other_op = other_op[0].lower() + other_op[1:]
            other_init = [default_init]
            for attr in attributes:
                lower_name = attr[0][0].lower() + attr[0][1:]
                private_name = lower_name + "_"
                other_init.append(
                    "{private_name}({other_op}.get{name}())".format(
                        name=attr[0], private_name=private_name, other_op=lower_other_op
                    )
                )
            init = dedent(
                """
                  {op}(const {other_op}& {lower_other_op}) :
                      {other_init} {{}}
                """.format(
                    op=op,
                    other_op=other_op,
                    lower_other_op=lower_other_op,
                    other_init=",\n      ".join(other_init),
                )
            )
            extra_init += init

    return dedent(
        """
        class {op} : public NeuralNetOperator {{
         public:
          {op}({attribute_args}) :
              {attribute_init} {{}}
          {extra_init}
          ~{op}() {{}}

          NOMNIGRAPH_DEFINE_NN_RTTI({op});
        {getters}{setters}
         private:
          {attribute_declarations}
        }};

        """.format(
            op=op,
            extra_init=extra_init,
            getters="".join(attribute_getters),
            setters="".join(attribute_setters),
            attribute_args=",\n".join(attribute_args),
            attribute_init=",\n".join(attribute_init),
            attribute_declarations="\n".join(attribute_declarations),
        )
    )
