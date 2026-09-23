def generate_transform(transform_list=[]):
    if len(transform_list):
        output = StringIO()
        for type, value in transform_list:
            if (type == 'scale' and (value == (1,) or value == (1, 1))
                    or type == 'translate' and value == (0, 0)
                    or type == 'rotate' and value == (0,)):
                continue
            if type == 'matrix' and isinstance(value, Affine2DBase):
                value = value.to_values()
            output.write('%s(%s)' % (
                type, ' '.join(short_float_fmt(x) for x in value)))
        return output.getvalue()
    return ''
