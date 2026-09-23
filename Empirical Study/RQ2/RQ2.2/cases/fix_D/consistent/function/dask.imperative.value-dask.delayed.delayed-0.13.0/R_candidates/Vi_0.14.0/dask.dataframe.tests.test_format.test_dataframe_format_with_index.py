def test_dataframe_format_with_index():
    df = pd.DataFrame({'A': [1, 2, 3, 4, 5, 6, 7, 8],
                       'B': list('ABCDEFGH'),
                       'C': pd.Categorical(list('AAABBBCC'))},
                      index=list('ABCDEFGH'))
    ddf = dd.from_pandas(df, 3)
    exp = ("Dask DataFrame Structure:\n"
           "                   A       B                C\n"
           "npartitions=3                                \n"
           "A              int64  object  category[known]\n"
           "D                ...     ...              ...\n"
           "G                ...     ...              ...\n"
           "H                ...     ...              ...\n"
           "Dask Name: from_pandas, 3 tasks")
    assert repr(ddf) == exp
    assert str(ddf) == exp

    exp_table = """<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
    </tr>
    <tr>
      <th>npartitions=3</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>A</th>
      <td>int64</td>
      <td>object</td>
      <td>category[known]</td>
    </tr>
    <tr>
      <th>D</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>G</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>H</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
  </tbody>
</table>"""

    exp = """<div><strong>Dask DataFrame Structure:</strong></div>
{exp_table}
<div>Dask Name: from_pandas, 3 tasks</div>""".format(exp_table=exp_table)
    assert ddf.to_html() == exp

    # table is boxed with div
    exp = """<div><strong>Dask DataFrame Structure:</strong></div>
<div>
{exp_table}
</div>
<div>Dask Name: from_pandas, 3 tasks</div>""".format(exp_table=exp_table)
    assert ddf._repr_html_() == exp
