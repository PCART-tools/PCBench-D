def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('_lsq', parent_package, top_path)
    config.add_extension('givens_elimination',
                         sources=['givens_elimination.c'])
    return config
