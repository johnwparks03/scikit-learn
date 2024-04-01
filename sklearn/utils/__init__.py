"""
The :mod:`sklearn.utils` module includes various utilities.
"""

import platform
import struct
from collections.abc import Sequence

import numpy as np

from ..exceptions import DataConversionWarning
from . import _joblib, metadata_routing
from ._bunch import Bunch
from ._chunking import gen_batches, gen_even_slices
from ._estimator_html_repr import estimator_html_repr

# Make _safe_indexing importable from here for backward compat as this particular
# helper is considered semi-private and typically very useful for third-party
# libraries that want to comply with scikit-learn's estimator API. In particular,
# _safe_indexing was included in our public API documentation despite the leading
# `_` in its name.
from ._indexing import (
    _safe_indexing,  # noqa
    resample,
    shuffle,
)
from ._mask import safe_mask
from .class_weight import compute_class_weight, compute_sample_weight
from .deprecation import deprecated
from .discovery import all_estimators
from .extmath import safe_sqr
from .murmurhash import murmurhash3_32
from .validation import (
    as_float_array,
    assert_all_finite,
    check_array,
    check_consistent_length,
    check_random_state,
    check_scalar,
    check_symmetric,
    check_X_y,
    column_or_1d,
    indexable,
)

# Do not deprecate parallel_backend and register_parallel_backend as they are
# needed to tune `scikit-learn` behavior and have different effect if called
# from the vendored version or or the site-package version. The other are
# utilities that are independent of scikit-learn so they are not part of
# scikit-learn public API.
parallel_backend = _joblib.parallel_backend
register_parallel_backend = _joblib.register_parallel_backend

__all__ = [
    "murmurhash3_32",
    "as_float_array",
    "assert_all_finite",
    "check_array",
    "check_random_state",
    "compute_class_weight",
    "compute_sample_weight",
    "column_or_1d",
    "check_consistent_length",
    "check_X_y",
    "check_scalar",
    "indexable",
    "check_symmetric",
    "deprecated",
    "parallel_backend",
    "register_parallel_backend",
    "resample",
    "shuffle",
    "all_estimators",
    "DataConversionWarning",
    "estimator_html_repr",
    "Bunch",
    "metadata_routing",
    "safe_sqr",
    "safe_mask",
    "gen_batches",
    "gen_even_slices",
]

IS_PYPY = platform.python_implementation() == "PyPy"
_IS_32BIT = 8 * struct.calcsize("P") == 32
_IS_WASM = platform.machine() in ["wasm32", "wasm64"]


def tosequence(x):
    """Cast iterable x to a Sequence, avoiding a copy if possible.

    Parameters
    ----------
    x : iterable
        The iterable to be converted.

    Returns
    -------
    x : Sequence
        If `x` is a NumPy array, it returns it as a `ndarray`. If `x`
        is a `Sequence`, `x` is returned as-is. If `x` is from any other
        type, `x` is returned casted as a list.
    """
    if isinstance(x, np.ndarray):
        return np.asarray(x)
    elif isinstance(x, Sequence):
        return x
    else:
        return list(x)
