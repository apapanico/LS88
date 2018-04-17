import warnings
warnings.filterwarnings("ignore")

from datascience import Table as _Table
import pandas as _pd
import numpy as _np
import matplotlib.pyplot as _plt


def verify_table(tbl, target):
    if isinstance(tbl, _Table):
        tbl = tbl.to_df()
        target = target.to_df()

    # check dimensions
    if tbl.shape != target.shape:
        print(f"input dims: {tbl.shape}, target dims: {target.shape}")
        return False

    for label in tbl.columns:
        # check labels
        if label not in target.columns:
            print(f"column {label} not in target")
            return False

        col = tbl[label]
        tgt_col = target[label]

        typ = col.dtype.type
        tgt_typ = tgt_col.dtype.type

        if issubclass(tgt_typ, _np.number):
            if not issubclass(typ, _np.number):
                print(f"column {label} not numeric")
                return False
            # check percision of numeric columns
            if not _np.allclose(col, tgt_col, atol=1e-6, equal_nan=True):
                print(f"column {label} values not correct")
                return False
        elif issubclass(tgt_typ, (_np.str, _np.object)):
            if not issubclass(typ, (_np.str, _np.object)):
                print(f"column {label} not string")
                return False
            # check percision of string columns
            if not _np.all(col == tgt_col):
                print(f"column {label} values not correct")
                return False

    return True


def head(table, n=5):
    return table.take[:n]


def scatterplot_by_x(table, x_columns, y_column, base_width=5, height=5,
                     sharey=True, title=None):
    if isinstance(table, _Table):
        table = table.to_df()
    ncols = len(x_columns)
    figsize = (ncols * base_width, height)
    fig, axarr = _plt.subplots(ncols=ncols, figsize=figsize, sharey=True)
    for i, x_label in enumerate(x_columns):
        table.plot.scatter(ax=axarr[i], x=x_label, y=y_column)

    if title is not None:
        fig.suptitle(title)


# def fill_null_values(table, column, fill_value=0):
#     return table.to_df()[column].fillna(fill_value, inplace=False)


# def fill_null(table, value=None, method=None):
#     df = table.to_df().fillna(value=value, method=method)
#     return _Table.from_df(df)


def fill_null(table, fill_column=None, fill_value=None, fill_method=None):
    if isinstance(table, _Table):
        table = table.to_df()
    data = table[fill_column] if fill_column is not None else table
    data = data.fillna(value=fill_value, method=fill_method)
    return data.values


def replace(table, column, to_replace, method='pad'):
    return table.to_df()[column].replace(
        to_replace, method=method, inplace=False)


def get_first_from_group(table, groupby):
    TABLE_FLAG = False
    if isinstance(table, _Table):
        TABLE_FLAG = True
        table = table.to_df()
    out = table.sort_values(groupby).\
        drop_duplicates(subset=groupby, keep='first')
    if TABLE_FLAG:
        return _Table.from_df(out)
    else:
        return out


def boxplots(table, column=None, by=None, ax=None, fontsize=None, rot=0,
             grid=True, figsize=None, layout=None, return_type=None,
             **kwds):
    if isinstance(table, _Table):
        table = table.to_df()

    table.boxplot(
        column=column, by=by, ax=ax, fontsize=fontsize, rot=rot,
        grid=grid, figsize=figsize, layout=layout, return_type=return_type
    )
    _plt.gcf().suptitle('')


def cut(col, bins, right=True, labels=None, retbins=False, precision=3,
        include_lowest=False):
    out = _pd.cut(
        col,
        bins,
        right=right,
        labels=labels,
        retbins=retbins,
        precision=precision,
        include_lowest=include_lowest
    )
    return out


def bucket(col, buckets, right=True, bucket_labels=None, retbuckets=False,
           precision=3, include_lowest=False):
    out = _pd.cut(
        col,
        buckets,
        right=right,
        labels=bucket_labels,
        retbins=retbuckets,
        precision=precision,
        include_lowest=include_lowest
    )
    return out


def concat(table_list):
    df = _pd.concat([t.to_df() for t in table_list])
    return _Table.from_df(df)


def multi_sort(table, by, descending=True, na_position='first'):
    sorted_df = table.to_df().sort_values(
        by, ascending=not descending, na_position=na_position)
    return _Table.from_df(sorted_df)


def sorted_boxplot(df, by, column, sort_order, figsize=(8, 6), fontsize=10):
    df2 = _pd.DataFrame({col: vals[column] for col, vals in df.groupby(by)})
    fig, ax = _plt.subplots(figsize=figsize)
    df2[sort_order].boxplot(rot=90, sym='', ax=ax, fontsize=fontsize)


def hexbin_plot(data, x, y, C=None, collect=None, gridsize=None, cmap=None,
                mincnt=None, vmin=None, vmax=None, **kwargs):
    if isinstance(data, _Table):
        data = data.to_df()
    hexbin = data.plot.hexbin(
        x=x, y=y, C=C, reduce_C_function=collect,
        gridsize=gridsize, cmap=cmap, mincnt=mincnt,
        vmin=vmin, vmax=vmax, **kwargs
    )
    hexbin.tick_params(reset=True)
    return hexbin
