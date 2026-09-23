def processor_name(processor):
    if hasattr(processor, 'name'):
        return processor.name
    if hasattr(processor, 'func_name'):
        if processor.func_name == '<lambda>':
            return processor.__module__
        if hasattr(processor, 'im_class'):
            return '%s.%s' % (processor.im_class.__name__, processor.func_name)
        return processor.func_name
    return processor.__class__.__name__
