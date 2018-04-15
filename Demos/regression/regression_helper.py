import numpy as _np
import pandas as _pd
import statsmodels.formula.api as _smf
import statsmodels.api as _sm
from scipy.sparse import coo_matrix as _coo_matrix
from sklearn import linear_model as _linear_model
import datascience as _ds


def multiple_regression(dep_var, ind_vars, data, constant=False,
                        interactions=None):
    if not isinstance(ind_vars, list):
        ind_vars = [ind_vars]
    formula = dep_var + '~' + (' + '.join(ind_vars))
    if constant:
        formula += ' + 1'
    else:
        formula += ' + 0'
    if interactions is not None:
        for (interact_1, interact_2) in interactions:
            formula += f' + {interact_1}:{interact_2}'
    results = _smf.ols(formula, data=data).fit()
    return results.params, results.fittedvalues, results.resid


def _sdf_to_coo(sdf, dtype=_np.float64):
    cols, rows, datas = [], [], []
    for col, name in enumerate(sdf):
        s = sdf[name]
        row = s.sp_index.to_int_index().indices
        cols.append(_np.repeat(col, len(row)))
        rows.append(row)
        datas.append(s.sp_values.astype(dtype, copy=False))

    cols = _np.concatenate(cols)
    rows = _np.concatenate(rows)
    datas = _np.concatenate(datas)
    return _coo_matrix((datas, (rows, cols)), shape=sdf.shape)


def _multiple_regression_with_penalty(dep_var, ind_vars, data, weights=None,
                                      penalty=0., constant=False, use_sparse=True):

    DS_FLAG = False
    if isinstance(data, _ds.Table):
        DS_FLAG = True
        data = data.to_df()
    if not isinstance(ind_vars, list):
        ind_vars = [ind_vars]
    if use_sparse:
        data = data.to_sparse(fill_value=0)
        X = _sdf_to_coo(data[ind_vars])
    else:
        X = data[ind_vars].values
    if weights is not None:
        w = data[weights].values
    y = data[dep_var].to_dense().values
    model = _linear_model.Ridge(
        alpha=penalty, fit_intercept=constant, copy_X=False)
    model.fit(X, y, sample_weight=w)
    if DS_FLAG:
        raise NotImplementedError('fill in datascience usage')
    else:
        coefs = _pd.Series(
            {var: coef for var, coef in zip(ind_vars, model.coef_)})
    return coefs


def multiple_regression_big(dep_var, ind_vars, data, weights=None,
                            constant=False):
    return _multiple_regression_with_penalty(
        dep_var, ind_vars, data, weights=weights, constant=constant)


def multiple_regression_big_with_penalty(dep_var, ind_vars, data, weights=None,
                                         penalty=0., constant=False):
    return _multiple_regression_with_penalty(
        dep_var, ind_vars, data, penalty=penalty,
        weights=weights, constant=constant)
