# Copyright (c) 2025 Nian Li
# This file is part of the IntensitySegments project and is licensed under the MIT License.
# See the LICENSE file or the project root for full license information.

"""
test_intensity_segments.py

Unit tests for the IntensitySegments class.

Author: Nian Li
Date: 2025-04-17
Email: linian2017t1@gmail.com
"""

import pytest
from intensity_segments.intensity_segments import IntensitySegments

def test_initial_segments():
    segments = IntensitySegments()
    assert str(segments) == "[]"

def test_add_basic():
    segments = IntensitySegments()
    segments.add(10, 30, 1)
    assert str(segments) == "[[10, 1], [30, 0]]"

    segments.add(20, 40, 1)
    assert str(segments) == "[[10, 1], [20, 2], [30, 1], [40, 0]]"

    segments.add(10, 40, -2)
    assert str(segments) == "[[10, -1], [20, 0], [30, -1], [40, 0]]"

def test_add_set_mixed():
    segments = IntensitySegments()
    segments.add(10, 30, 1)
    assert str(segments) == "[[10, 1], [30, 0]]"

    segments.add(20, 40, 1)
    assert str(segments) == "[[10, 1], [20, 2], [30, 1], [40, 0]]"

    segments.add(10, 40, -1)
    assert str(segments) == "[[20, 1], [30, 0]]"

    segments.add(10, 40, -1)
    assert str(segments) == "[[10, -1], [20, 0], [30, -1], [40, 0]]"

def test_set_basic():
    segments = IntensitySegments()
    segments.set(10, 30, 5)
    assert str(segments) == "[[10, 5], [30, 0]]"

    segments.add(20, 40, 2)
    assert str(segments) == "[[10, 5], [20, 7], [30, 2], [40, 0]]"

def test_no_op_ranges():
    segments = IntensitySegments()
    segments.add(10, 10, 5)  # No-op
    assert str(segments) == "[]"

    segments.set(20, 20, 3)  # No-op
    assert str(segments) == "[]"

def test_multiple_operations():
    segments = IntensitySegments()
    segments.add(0, 100, 1)
    segments.set(20, 30, 5)
    segments.add(25, 35, 2)

    assert str(segments) == "[[0, 1], [20, 5], [25, 7], [30, 3], [35, 1], [100, 0]]"
