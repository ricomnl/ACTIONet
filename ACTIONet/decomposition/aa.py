"""Archetypal analysis for dense matrices.
"""
import numpy as np
import _ACTIONet as _an
import ACTIONet as an

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn._config import config_context


class ArchetypalAnalysis(TransformerMixin, BaseEstimator):
    """Dimensionality reduction using archetypal analysis.
    This transformer performs archetypal analysis (AA) on input data.

    The objective function is:
       .. math::
            0.5 * ||X - XCH||_{loss}^2
    Where:
        :math: W = XC,
        :math: 0 <= C_ij, H_ij,
        :math: \sum_{i} C_ij = 1,
        :math: \sum_{i} H_ij = 1,

    Parameters
    ----------
    n_components : int, default=None
        Number of components, if n_components is not set all features
        are kept.

    n_iter : int, default=100
        Number of iterations for AA solver.

    tol : float, default=1e-6
        Tolerance of the stopping condition.


    Attributes
    ----------
    components_ : ndarray of shape (n_components, n_features)
        Factorization matrix, sometimes called 'dictionary'.
    n_components_ : int
        The number of components. It is same as the `n_components` parameter
        if it was given. Otherwise, it will be same as the number of
        features.

    References
    ----------
    A geometric approach to characterize the functional identity of single cells
    Mohamadi, et al., 2018 https://www.nature.com/articles/s41467-018-03933-2

    Examples
    --------
    >>> from decomp import AA
    >>> aa = AA(n_components=5, n_iter=7)
    >>> aa.fit(X)
    aa(n_components=5, n_iter=7)
    >>> print(aa.components_)
    """

    def __init__(self, n_components=2, *, n_iter=100, tol=1e-16):
        self.n_components = n_components
        self.n_iter = n_iter
        self.tol = tol

    def fit(self, X, y=None, **params):
        """Learn a AA model for the data X.
        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            Training vector, where `n_samples` is the number of samples
            and `n_features` is the number of features.
        y : Ignored
            Not used, present for API consistency by convention.
        **params : kwargs
            Parameters (keyword arguments) and values passed to
            the fit_transform instance.
        Returns
        -------
        self : object
            Returns the instance itself.
        """
        self.fit_transform(X, **params)
        return self

    def fit_transform(self, X, y=None, W0=None):
        """Learn an ACTION model for the data X and returns the transformed data.
        This is more efficient than calling fit followed by transform.
        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            Training vector, where `n_samples` is the number of samples
            and `n_features` is the number of features.
        y : Ignored
            Not used, present for API consistency by convention.
        W0 : array-like of shape (n_samples, n_components)
           Used as initial guess for the solution.
        Returns
        -------
        W : ndarray of shape (n_samples, n_components)
            Transformed data.
        """
        X = self._validate_data(X, accept_sparse=False)

        if W0 is None:
            spa = an.decomp.SPA(self.n_components)
            W0 = spa.fit_transform(X)

        with config_context(assume_finite=True):
            out = self._fit_transform(X, W0=W0)

        W, H = out["W"], out["H"]
        self.coeff = out["C"]
        self.n_components_ = H.shape[0]
        self.components_ = H

        return W

    def _fit_transform(self, X, y=None, W0=None):
        """Learn a AA model for the data X and returns the transformed data.
        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            Data matrix to be decomposed
        y : Ignored
        W : array-like of shape (n_samples, n_components)
            Used as initial guess for the solution.
        update_H : bool, default=True
            If True, both W and H will be estimated from initial guesses,
            this corresponds to a call to the 'fit_transform' method.
            If False, only W will be estimated, this corresponds to a call
            to the 'transform' method.
        Returns
        -------
        W : ndarray of shape (n_samples, n_components)
            Transformed data.
        H : ndarray of shape (n_components, n_features)
            Factorization matrix, sometimes called 'dictionary'.
        """
        out = _an.run_AA(X, W0, self.n_iter, self.tol)

        return out
