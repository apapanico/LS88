import warnings
warnings.filterwarnings("ignore")

from datascience import Table as _Table
import numpy as _np
import matplotlib.pyplot as _plt
from matplotlib.ticker import MultipleLocator as _MultipleLocator
from matplotlib.collections import PolyCollection as _PC
from matplotlib.colors import LinearSegmentedColormap as _LinearSegmentedColormap
from matplotlib.cm import register_cmap as _register_cmap
from IPython.display import display as _display

cmap = _plt.get_cmap('Dark2')
cmap_4thdownbot = _LinearSegmentedColormap.from_list(
    '4thdownbot_cmap', cmap.colors[:3], N=3)
_register_cmap(name='4thdownbot_cmap', cmap=cmap_4thdownbot)


def display_re_matrix(re):
    _display(re.unstack(level=0).sort_values(by=0))


def display_weights(w):
    _display(w.to_frame().transpose())


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


def prettify_4thdownbot(data, ax, annotate=True, colorbar=False):
    ax.imshow(data, alpha=.6, cmap='4thdownbot_cmap', aspect='auto',
              origin='lower', extent=(1, 100, -.5, 8.5))

    ax.set_xlim(-.25, 100.25)
    ax.set_xticks(
        _np.array([-.5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 99.5]) + .5)
    ax.set_xticklabels(['Your\nGoal', '10', '20', '30', '40',
                        '50', '40', '30', '20', '10', 'Opp\nGoal'])
    ax.tick_params(axis='both', which='major', labelsize=15)
    minorLocator = _MultipleLocator(1)
    ax.xaxis.set_minor_locator(minorLocator)
    ax.grid(b=True, which='minor', axis='x')
    ax.grid(b=False, which='major', axis='x')

    ax.set_ylim(-0.54, 8.54)
    ax.set_yticks([
        yd - .5
        for yd in range(1, 10)
    ])
    ax.set_yticks([
        yd - 1
        for yd in range(1, 10)
    ], minor=True)
    ax.set_yticklabels([
        '4th and {}'.format(yd)
        for yd in range(9, 0, -1)
    ], minor=True)
    _plt.setp(ax.get_yticklabels(), visible=False)
    _plt.setp(ax.get_yticklabels(minor=True), visible=True)

    if annotate:
        ax.text(50, 6, 'Go for it', size=25)
        ax.text(20, 1.5, 'Punt', size=25)
        ax.text(75, 1.5, 'Kick', size=25)

    if colorbar:
        PCM = list(filter(lambda c: isinstance(c, _PC), ax.get_children()))[0]
        cbar = _plt.colorbar(PCM, ticks=[4 / 3, 2, 8 / 3])
        cbar.ax.set_yticklabels(['Go for it', 'Punt', 'Kick'], fontsize=15)
