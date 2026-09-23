def configuration(parent_name='special', top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('_precompute', parent_name, top_path)
    return config
