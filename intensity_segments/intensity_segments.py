# Copyright (c) 2025 Nian Li
# This file is part of the IntensitySegments project and is licensed under the MIT License.
# See the LICENSE file or the project root for full license information.

"""
intensity_segments.py

This module implements the IntensitySegments class, which manages intensity values over infinite intervals.
It allows adding and setting intensity values in given ranges, starting from an initial intensity of 0,
using a SortedDict for efficient and clean updates.

Author: Nian Li
Date: 2025-04-17
Email: linian2017t1@gmail.com
"""

from sortedcontainers import SortedDict

class IntensitySegments:
    """
    A class to manage and update intensity values across continuous segments.

    Attributes:
        segments (SortedDict[int, int]): A sorted dictionary mapping start points to intensity values.

    Methods:
        add(from_, to, amount):
            Adds an intensity amount to the specified range [from_, to).

        set(from_, to, amount):
            Sets the intensity to a specific value for the specified range [from_, to).

        __str__():
            Returns a compact string representation of the current segments.
    """

    def __init__(self) -> None:
        """
        Initialize the IntensitySegments with an empty sorted dictionary of segments.
        """
        self.segments: SortedDict[int, int] = SortedDict()

    def _ensure_point(self, point: int) -> None:
        """
        Helper to ensure a point exists in the segments.

        If the point is not already a start point, copy intensity from the previous segment.
        """
        if point not in self.segments:
            if not self.segments:
                self.segments[point] = 0
            else:
                idx = self.segments.bisect_left(point)
                if idx == 0:
                    self.segments[point] = 0
                else:
                    prev_key = list(self.segments.keys())[idx - 1]
                    self.segments[point] = self.segments[prev_key]

    def add(self, from_: int, to: int, amount: int) -> None:
        """
        Add an intensity amount to the specified range [from_, to).

        Args:
            from_ (int): Start of the range (inclusive).
            to (int): End of the range (exclusive).
            amount (int): Amount to add to the intensity.

        Returns:
            None
        """
        if from_ >= to:
            return

        self._ensure_point(from_)
        self._ensure_point(to)

        keys = list(self.segments.irange(from_, to, inclusive=(True, False)))
        for key in keys:
            self.segments[key] += amount

        self._cleanup()

    def set(self, from_: int, to: int, amount: int) -> None:
        """
        Set the intensity to a specific value for the specified range [from_, to).

        Args:
            from_ (int): Start of the range (inclusive).
            to (int): End of the range (exclusive).
            amount (int): New intensity value to set.

        Returns:
            None
        """
        if from_ >= to:
            return

        self._ensure_point(from_)
        self._ensure_point(to)

        keys = list(self.segments.irange(from_, to, inclusive=(True, False)))
        for key in keys:
            self.segments[key] = amount

        self._cleanup()

    def _cleanup(self) -> None:
        """
        Merge adjacent segments with the same intensity to keep the representation compact.
        Remove unnecessary [start, 0] segments at the beginning.
        """
        prev_key = None
        keys_to_delete = []

        for key in self.segments.keys():
            if prev_key is not None and self.segments[prev_key] == self.segments[key]:
                keys_to_delete.append(key)
            else:
                prev_key = key

        for key in keys_to_delete:
            del self.segments[key]

        # Additional cleanup: if the first segment is [x, 0] and it's unnecessary, remove it
        keys = list(self.segments.keys())
        if keys and keys[0] != 0 and self.segments[keys[0]] == 0:
            del self.segments[keys[0]]

    def __str__(self) -> str:
        """
        Return a compact string representation of the current segments.

        Returns:
            str: String formatted list of [start, intensity] pairs.
        """
        items = [[k, v] for k, v in self.segments.items()]
        return str(items)