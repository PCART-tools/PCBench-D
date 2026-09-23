def test_dataframe_format_long():
    df = pd.DataFrame({'A': [1, 2, 3, 4, 5, 6, 7, 8] * 10,
                       'B': list('ABCDEFGH') * 10,
                       'C': pd.Categorical(list('AAABBBCC') * 10)})
    ddf = dd.from_pandas(df, 10)
    exp = ('Dask DataFrame Structure:\n'
           '                    A       B                C\n'
           'npartitions=10                                \n'
           '0               int64  object  category[known]\n'
           '8                 ...     ...              ...\n'
           '...               ...     ...              ...\n'
           '72                ...     ...              ...\n'
           '79                ...     ...              ...\n'
           'Dask Name: from_pandas, 10 tasks')
    assert repr(ddf) == exp
    assert str(ddf) == exp

    exp = ("                    A       B                C\n"
           "npartitions=10                                \n"
           "0               int64  object  category[known]\n"
           "8                 ...     ...              ...\n"
           "...               ...     ...              ...\n"
           "72                ...     ...              ...\n"
           "79                ...     ...              ...")
    assert ddf.to_string() == exp

    exp_table = """<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
    </tr>
    <tr>
      <th>npartitions=10</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>int64</td>
      <td>object</td>
      <td>category[known]</td>
    </tr>
    <tr>
      <th>8</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>72</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>79</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
  </tbody>
</table>"""

    exp = """<div><strong>Dask DataFrame Structure:</strong></div>
{exp_table}
<div>Dask Name: from_pandas, 10 tasks</div>""".format(exp_table=exp_table)
    assert ddf.to_html() == exp

    # table is boxed with div
    exp = u"""<div><strong>Dask DataFrame Structure:</strong></div>
<div>
{exp_table}
</div>
<div>Dask Name: from_pandas, 10 tasks</div>""".format(exp_table=exp_table)
    assert ddf._repr_html_() == exp
