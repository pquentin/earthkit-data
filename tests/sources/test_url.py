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

from earthkit.data import from_source, settings
from earthkit.data.core.temporary import temp_directory
from earthkit.data.testing import earthkit_file, network_off


@pytest.mark.skipif(  # TODO: fix
    sys.platform == "win32",
    reason="file:// not working on Windows yet",
)
def test_url_file_source():
    filename = os.path.abspath(earthkit_file("docs/examples/test.nc"))
    s = from_source("url", f"file://{filename}")
    assert len(s) == 2


def test_url_source_1():
    from_source(
        "url", "https://get.ecmwf.int/repository/test-data/emohawk/examples/test.grib"
    )


def test_url_source_check_out_of_date():
    def load():
        from_source(
            "url",
            "https://get.ecmwf.int/repository/test-data/emohawk/examples/test.grib",
        )

    with temp_directory() as tmpdir:
        with settings.temporary():
            settings.set("cache-directory", tmpdir)
            load()

            settings.set("check-out-of-date-urls", False)
            with network_off():
                load()


def test_url_source_2():
    from_source(
        "url",
        "https://get.ecmwf.int/repository/test-data/emohawk/test-data/temp.bufr",
    )


def test_url_source_3():
    from_source(
        "url",
        "https://get.ecmwf.int/repository/test-data/emohawk/examples/test.nc",
    )


def test_url_source_tar():
    ds = from_source(
        "url",
        "https://get.ecmwf.int/repository/test-data/emohawk/examples/test_gribs.tar",
    )
    assert len(ds) == 6


def test_part_url():
    ds = from_source(
        "url",
        "https://get.ecmwf.int/repository/test-data/emohawk/test-data/temp.bufr",
    )

    ds = from_source(
        "url",
        "https://get.ecmwf.int/repository/test-data/emohawk/test-data/temp.bufr",
        parts=((0, 4),),
    )

    assert os.path.getsize(ds.path) == 4

    with open(ds.path, "rb") as f:
        assert f.read() == b"BUFR"

    ds = from_source(
        "url",
        "https://get.ecmwf.int/repository/test-data/emohawk/test-data/temp.bufr",
        parts=((0, 10), (50, 10), (60, 10)),
    )

    print(ds.path)

    assert os.path.getsize(ds.path) == 30

    with open(ds.path, "rb") as f:
        assert f.read()[:4] == b"BUFR"


@pytest.mark.skipif(  # TODO: fix
    sys.platform == "win32",
    reason="file:// not working on Windows yet",
)
def test_url_part_file_source():
    filename = os.path.abspath(earthkit_file("docs/examples/test.grib"))
    ds = from_source(
        "url",
        f"file://{filename}",
        parts=[
            (0, 4),
            (522, 4),
            (526, 4),
            (1048, 4),
        ],
    )

    assert os.path.getsize(ds.path) == 16

    with open(ds.path, "rb") as f:
        assert f.read() == b"GRIB7777GRIB7777"


if __name__ == "__main__":
    test_part_url()
    # from earthkit.data.testing import main

    # main(__file__)
