# (C) Copyright 2022 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.


try:
    # NOTE: the `version.py` file must not be present in the git repository
    #   as it is generated by setuptools at install time
    from .version import __version__
except ImportError:  # pragma: no cover
    # Local copy or not installed with setuptools
    __version__ = "999"

from .arguments.transformers import ALL
from .core.caching import CACHE as cache
from .core.settings import SETTINGS as settings
from .sources import from_source, from_source_lazily

__all__ = [
    "ALL",
    "cache",
    "from_source",
    "from_source_lazily",
    "settings",
    "__version__",
]
