def get_output(o, i):
    if len(o['returns']) == 1:
        return 'the_result'
    else:
        return '::std::get<{}>(the_result)'.format(i)
