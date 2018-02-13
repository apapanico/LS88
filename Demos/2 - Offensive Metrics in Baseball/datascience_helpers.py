import warnings
warnings.filterwarnings("ignore")

from datascience import Table as _Table
import pandas as _pd
import matplotlib.pyplot as _plt
from matplotlib.collections import PolyCollection as _PC
from matplotlib.colors import LinearSegmentedColormap as _LinearSegmentedColormap
from matplotlib.cm import register_cmap as _register_cmap
from scipy.stats import pearsonr as _pearsonr
import statsmodels.api as _sm
from IPython.display import display


cmap = _plt.get_cmap('Dark2')
cmap_4thdownbot = _LinearSegmentedColormap.from_list(
    '4thdownbot_cmap', cmap.colors[:3], N=3)
_register_cmap(name='4thdownbot_cmap', cmap=cmap_4thdownbot)


def correlation(x, y):
    rho = _pearsonr(x, y)[0]
    return rho


def linear_fit(x, y, constant=True):
    if constant:
        x = _sm.add_constant(x)
    fit = _sm.OLS(y, x).fit()
    out = (fit.params, fit.fittedvalues, fit.resid)
    return out


def display_re_matrix(re):
    display(re.unstack(level=0).sort_values(by=0))


def display_weights(w):
    display(w.to_frame().transpose())


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


def fast_run_expectancy(retro, re):
    TABLE_FLAG = False
    if isinstance(retro, _Table):
        TABLE_FLAG = True
        retro = retro.to_df()
        re = re.to_df().set_index(['Outs', 'Start_Bases'])

    # Build current out-runner states
    idx = list(zip(retro['Outs'], retro['Start_Bases']))
    # Extract run potentials
    retro['Run_Expectancy'] = re.loc[idx].values

    next_outs = retro['Outs'] + retro['Event_Outs']
    # Build next out-runner states
    idx = list(zip(next_outs, retro['End_Bases']))
    # Extract run potentials
    retro['Run_Expectancy_Next'] = re.loc[idx].values

    # When the inning ends, there are 3 outs.  That is not in the run
    # expectancy matrix so inning ending plate appearances will have an NA
    # value here.  We fill those with 0.
    retro['Run_Expectancy_Next'].fillna(0, inplace=True)

    return _Table.from_df(retro) if TABLE_FLAG else retro


def most_common_lineup_position(retro):
    TABLE_FLAG = False
    if isinstance(retro, _Table):
        TABLE_FLAG = True
        retro = retro.to_df()

    # Order of operations:
    # 1. Get PA counts
    # 2. Turn Lineup_Order into a column
    # 3. Rename column to PA
    # 4. Sort on PA in descending order
    lineup_pos = retro.groupby(['Batter_ID', 'Lineup_Order'])['Inning'].\
        count().\
        reset_index(level='Lineup_Order').\
        rename(columns={'Inning': 'PA'}).\
        sort_values('PA', ascending=False)
    # Duplicates indicate other positions.  By keeping first, we keep the most
    # common due to the sorting
    most_common = ~lineup_pos.index.duplicated(keep='first')
    lineup_pos = lineup_pos.loc[most_common, ['Lineup_Order']].sort_index()

    if TABLE_FLAG:
        return _Table.from_df(lineup_pos.reset_index())
    else:
        return lineup_pos


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


def prettify_4thdownbot(ax, annotate=False, colorbar=False):
    ax.set_xticks([1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 99])
    ax.set_xticklabels(['Your\nGoal', '10', '20', '30', '40',
                        '50', '40', '30', '20', '10', 'Opp\nGoal'])
    ax.set_yticks([
        yd - .5
        for yd in range(1, 10)
    ])
    ax.set_yticklabels([
        '4th and {}'.format(yd)
        for yd in range(9, 0, -1)
    ])
    if annotate:
        ax.text(50, 6, 'Go for it', size=25)
        ax.text(20, 1.5, 'Punt', size=25)
        ax.text(75, 1.5, 'Kick', size=25)
    ax.tick_params(axis='both', which='major', labelsize=15)

    if colorbar:
        PCM = list(filter(lambda c: isinstance(c, _PC), ax.get_children()))[0]
        cbar = _plt.colorbar(PCM, ticks=[4 / 3, 2, 8 / 3])
        cbar.ax.set_yticklabels(['Go for it', 'Punt', 'Kick'], fontsize=15)
