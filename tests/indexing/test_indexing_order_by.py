#!/usr/bin/env python3

# (C) Copyright 2020 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

import os
import sys

import pytest

here = os.path.dirname(__file__)
sys.path.insert(0, here)
from indexing_fixtures import check_sel_and_order, get_fixtures  # noqa: E402


@pytest.mark.parametrize("params", (["t", "u"], ["u", "t"]))
@pytest.mark.parametrize("levels", ([500, 850], [850, 500]))
@pytest.mark.parametrize("input_mode", ["directory", "list-of-dicts"])
@pytest.mark.parametrize("indexing", [True])
def test_indexing_order_by_with_request(params, levels, input_mode, indexing):
    request = dict(
        level=levels,
        variable=params,
        time="1200",
    )

    ds, _, total, n = get_fixtures(input_mode, indexing, request)

    for i in ds:
        print(i)
    assert len(ds) == 4, len(ds)

    check_sel_and_order(ds, params, levels)


@pytest.mark.parametrize("params", (["t", "u"], ["u", "t"]))
@pytest.mark.parametrize("levels", ([500, 850], [850, 500]))
@pytest.mark.parametrize("input_mode", ["directory", "file", "list-of-dicts"])
@pytest.mark.parametrize("indexing", [True])
def test_indexing_order_by_with_keyword(params, levels, input_mode, indexing):
    request = dict(variable=params, level=levels, date=20180801, time="1200")
    request["order_by"] = dict(level=levels, variable=params)

    ds, _, total, n = get_fixtures(input_mode, indexing, request)

    assert len(ds) == n, len(ds)

    check_sel_and_order(ds, params, levels)


@pytest.mark.parametrize("params", (["t", "u"],))
@pytest.mark.parametrize("levels", ([500, 850],))
@pytest.mark.parametrize("input_mode", ["directory", "file", "list-of-dicts"])
@pytest.mark.parametrize("indexing", [True, False])
def test_indexing_order_by_with_method_with_list(params, levels, input_mode, indexing):
    request = dict(variable=params, level=levels, date=20180801, time="1200")
    order_by = ["level", "variable"]

    ds, _, total, n = get_fixtures(input_mode, indexing, {})

    assert len(ds) == total, len(ds)

    ds = ds.sel(**request)
    assert len(ds) == n, len(ds)

    ds = ds.order_by(order_by)
    assert len(ds) == n

    check_sel_and_order(ds, params, levels)


@pytest.mark.parametrize("params", (["t", "u"], ["u", "t"]))
@pytest.mark.parametrize("levels", ([500, 850], [850, 500]))
@pytest.mark.parametrize("input_mode", ["directory", "file", "list-of-dicts"])
@pytest.mark.parametrize("indexing", [True, False])
def test_indexing_order_by_with_method(params, levels, input_mode, indexing):
    request = dict(variable=params, level=levels, date=20180801, time="1200")
    order_by = dict(level=levels, variable=params)

    ds, _, total, n = get_fixtures(input_mode, indexing, {})

    print(ds)
    print()
    for i in ds:
        print(i)
    assert len(ds) == total, len(ds)

    ds = ds.sel(**request)
    assert len(ds) == n, len(ds)

    ds = ds.order_by(order_by)
    assert len(ds) == n

    check_sel_and_order(ds, params, levels)

    keys = list(ds.coords.keys())
    assert keys == ["levelist", "param"], keys
    coords_params = list(ds.coords["param"])
    coords_levels = list(ds.coords["levelist"])
    coords_levels = [int(x) for x in coords_levels]
    assert coords_params == params, (coords_params, params)
    assert coords_levels == levels, (coords_levels, levels)


@pytest.mark.parametrize("params", (["t", "u"], ["u", "t"]))
@pytest.mark.parametrize(
    "levels", ([500, 850], [850, 500], ["500", "850"], ["850", "500"])
)
@pytest.mark.parametrize("input_mode", ["directory"])
@pytest.mark.parametrize("indexing", [True])
def test_indexing_order_ascending_descending(params, levels, input_mode, indexing):
    request = dict(variable=params, level=levels, date=20180801, time="1200")
    order_by = dict(level="descending", variable="ascending")

    ds, _, total, n = get_fixtures(input_mode, indexing, {})

    ds = ds.sel(**request)
    assert len(ds) == 4, len(ds)

    ds = ds.order_by(order_by)
    assert len(ds) == 4

    assert ds[0].metadata("param") == min(params)
    assert ds[1].metadata("param") == max(params)
    assert ds[2].metadata("param") == min(params)
    assert ds[3].metadata("param") == max(params)

    assert int(ds[0].metadata("level")) == max([int(x) for x in levels])
    assert int(ds[1].metadata("level")) == max([int(x) for x in levels])
    assert int(ds[2].metadata("level")) == min([int(x) for x in levels])
    assert int(ds[3].metadata("level")) == min([int(x) for x in levels])
    print()


if __name__ == "__main__":
    from earthkit.data.testing import main

    main(__file__)
