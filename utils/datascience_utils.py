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


def scatter_by_x(table, x_columns, y_column, base_width=5, height=5,
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


def fill_null_values(table, column, fill_value=0):
    return table.to_df()[column].fillna(fill_value, inplace=False)


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


def fill_null(table, value=None, method=None):
    df = table.to_df().fillna(value=value, method=method)
    return _Table.from_df(df)


def curve_fit(x, y, smoothness=.5):
    from statsmodels.nonparametric.smoothers_lowess import lowess
    results = lowess(y, x, is_sorted=True, frac=smoothness)
    return results[:, 1]


def concat(table_list):
    df = _pd.concat([t.to_df() for t in table_list])
    return _Table.from_df(df)


def multi_sort(table, by, descending=True, na_position='first'):
    sorted_df = table.to_df().sort_values(
        by, ascending=not descending, na_position=na_position)
    return _Table.from_df(sorted_df)
