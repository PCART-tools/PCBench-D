@Appender(_shared_docs['boxplot'] % _shared_doc_kwargs)
def boxplot(self, column=None, by=None, ax=None, fontsize=None,
            rot=0, grid=True, figsize=None, layout=None, return_type=None,
            **kwds):
    import pandas.tools.plotting as plots
    import matplotlib.pyplot as plt
    ax = plots.boxplot(self, column=column, by=by, ax=ax,
                       fontsize=fontsize, grid=grid, rot=rot,
                       figsize=figsize, layout=layout, return_type=return_type,
                       **kwds)
    plt.draw_if_interactive()
    return ax
