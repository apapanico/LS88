import warnings
warnings.filterwarnings("ignore")

from scipy.stats import pearsonr as _pearsonr
import statsmodels.api as _sm


def correlation(x, y):
    rho = _pearsonr(x, y)[0]
    return rho


def linear_fit(x, y, constant=True):
    if constant:
        x = _sm.add_constant(x)
    fit = _sm.OLS(y, x).fit()
    out = (fit.params, fit.fittedvalues, fit.resid)
    return out

def curve_fit(x, y, smoothness=.5):
    from statsmodels.nonparametric.smoothers_lowess import lowess
    results = lowess(y, x, is_sorted=True, frac=smoothness)
    return results[:, 1]
