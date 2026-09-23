def dump_plot(df, sizes):
    keys = []
    vals = []
    indexed = df[df['N'] == df['M']]
    for index, row in indexed.iterrows():
        keys.append(row['name'])
        vals.append(row['ratio'])

    keys = keys[::len(sizes)]
    sns.set(rc={'figure.figsize' : (5.0, len(keys) * 0.5)})

    cmap = sns.diverging_palette(10, 120, n=9, as_cmap=True)
    np_vals = np.array([vals]).reshape(-1, len(sizes))
    g = sns.heatmap(np_vals, annot=True, cmap=cmap, center=1.0, yticklabels=True)
    plt.yticks(rotation=0)
    plt.title('PyTorch performance divided by NNC performance (single core)')
    plt.xlabel('Size of NxN matrix')
    plt.ylabel('Operation')
    g.set_yticklabels(keys)
    g.set_xticklabels(sizes)

    plt.savefig('nnc.png')
