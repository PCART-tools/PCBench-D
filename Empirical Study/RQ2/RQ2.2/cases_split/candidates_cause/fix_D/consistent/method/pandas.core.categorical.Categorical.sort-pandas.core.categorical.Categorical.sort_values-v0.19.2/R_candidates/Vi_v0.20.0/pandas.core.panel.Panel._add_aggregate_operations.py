    @classmethod
    def _add_aggregate_operations(cls, use_numexpr=True):
        """ add the operations to the cls; evaluate the doc strings again """

        # doc strings substitors
        _agg_doc = """
Wrapper method for %%s

Parameters
----------
other : %s or %s""" % (cls._constructor_sliced.__name__, cls.__name__) + """
axis : {""" + ', '.join(cls._AXIS_ORDERS) + "}" + """
    Axis to broadcast over

Returns
-------
""" + cls.__name__ + "\n"

        def _panel_arith_method(op, name, str_rep=None, default_axis=None,
                                fill_zeros=None, **eval_kwargs):
            def na_op(x, y):
                try:
                    result = expressions.evaluate(op, str_rep, x, y,
                                                  raise_on_error=True,
                                                  **eval_kwargs)
                except TypeError:
                    result = op(x, y)

                # handles discrepancy between numpy and numexpr on division/mod
                # by 0 though, given that these are generally (always?)
                # non-scalars, I'm not sure whether it's worth it at the moment
                result = missing.fill_zeros(result, x, y, name, fill_zeros)
                return result

            if name in _op_descriptions:
                op_name = name.replace('__', '')
                op_desc = _op_descriptions[op_name]
                if op_desc['reversed']:
                    equiv = 'other ' + op_desc['op'] + ' panel'
                else:
                    equiv = 'panel ' + op_desc['op'] + ' other'

                _op_doc = """
                %%s of series and other, element-wise (binary operator `%%s`).
                Equivalent to ``%%s``.

                Parameters
                ----------
                other : %s or %s""" % (cls._constructor_sliced.__name__,
                                       cls.__name__) + """
                axis : {""" + ', '.join(cls._AXIS_ORDERS) + "}" + """
                    Axis to broadcast over

                Returns
                -------
                """ + cls.__name__ + """

                See also
                --------
                """ + cls.__name__ + ".%s\n"
                doc = _op_doc % (op_desc['desc'], op_name, equiv,
                                 op_desc['reverse'])
            else:
                doc = _agg_doc % name

            @Appender(doc)
            def f(self, other, axis=0):
                return self._combine(other, na_op, axis=axis)

            f.__name__ = name
            return f

        # add `div`, `mul`, `pow`, etc..
        ops.add_flex_arithmetic_methods(
            cls, _panel_arith_method, use_numexpr=use_numexpr,
            flex_comp_method=ops._comp_method_PANEL)
