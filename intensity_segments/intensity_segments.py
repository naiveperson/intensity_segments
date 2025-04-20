# Copyright (c) 2025 Nian Li
# This file is part of the IntensitySegments project and is licensed under the MIT License.
# See the LICENSE file or the project root for full license information.

"""
intensity_segments.py

This module implements the IntensitySegments class, which manages intensity values over infinite intervals.
It allows adding and setting intensity values in given ranges, starting from an initial intensity of 0,
using list as internal storage and binary search wherever necessary for efficient updates.
The current time complexity is O(n) on average, advanced data structure like Skip List or AVL tree can be used for better performance.

Author: Nian Li
Date: 2025-04-17
Email: linian2017t1@gmail.com
"""

class IntensitySegments:
    """
    Manage intensity values across continuous segments using sorted list and binary search.

    Attributes:
        segments (list[list[int, int]]): Sorted list of [start, intensity].

    Methods:
        add(from_, to, amount):
            Adds intensity amount to range [from_, to).

        set(from_, to, amount):
            Sets intensity to amount for range [from_, to).

        __str__():
            Returns a compact string representation of the segments.
    """

    def __init__(self) -> None:
        """
        Initialize an empty list of segments.
        """
        self.segments: list[list[int, int]] = []

    def _find_index(self, point: int) -> int:
        """
        Binary search to find the index of the first segment whose start >= point.
        """
        lo, hi = 0, len(self.segments)
        while lo < hi:
            mid = (lo + hi) // 2
            if self.segments[mid][0] < point:
                lo = mid + 1
            else:
                hi = mid
        return lo

    def _ensure_point(self, point: int) -> None:
        """
        Ensure that a segment starting at 'point' exists.
        If not, insert it with the correct intensity.
        """
        idx = self._find_index(point)

        if idx < len(self.segments) and self.segments[idx][0] == point:
            return  # Already exists

        value = 0 if idx == 0 else self.segments[idx - 1][1]
        self.segments.insert(idx, [point, value])

    def add(self, from_: int, to: int, amount: int) -> None:
        """
        Add intensity amount to range [from_, to).

        Args:
            from_ (int): Start of the range (inclusive).
            to (int): End of the range (exclusive).
            amount (int): Amount to add.
        """
        if from_ >= to:
            return

        self._ensure_point(from_)
        self._ensure_point(to)

        idx = self._find_index(from_)
        while idx < len(self.segments) and self.segments[idx][0] < to:
            self.segments[idx][1] += amount
            idx += 1

        self._cleanup_local(from_, to)

    def set(self, from_: int, to: int, amount: int) -> None:
        """
        Set intensity to a fixed amount over range [from_, to).

        Args:
            from_ (int): Start of the range (inclusive).
            to (int): End of the range (exclusive).
            amount (int): New intensity value.
        """
        if from_ >= to:
            return

        self._ensure_point(from_)
        self._ensure_point(to)

        idx = self._find_index(from_)
        while idx < len(self.segments) and self.segments[idx][0] < to:
            self.segments[idx][1] = amount
            idx += 1

        self._cleanup_local(from_, to)

    def _cleanup_local(self, from_: int, to: int) -> None:
        """
        Locally merge segments between from_ and to to keep representation compact,
        and correctly remove redundant zero intensity segments.
        """
        if not self.segments:
            return

        start_idx = max(self._find_index(from_) - 1, 0)
        end_idx = min(self._find_index(to), len(self.segments))

        cleaned = self.segments[:start_idx+1]

        i = start_idx + 1
        while i < end_idx:
            if cleaned and cleaned[-1][1] == self.segments[i][1]:
                i += 1
                continue
            cleaned.append(self.segments[i])
            i += 1

        cleaned.extend(self.segments[end_idx:])

        # Remove unnecessary leading zeros
        while len(cleaned) > 1 and cleaned[0][1] == 0:
            cleaned.pop(0)

        # Remove unnecessary ending zeros (keep the last one)
        while len(cleaned) > 1 and cleaned[-1][1] == 0 and cleaned[-2][1] == 0:
            cleaned.pop()

        self.segments = cleaned


    def __str__(self) -> str:
        """
        Return a string representation of the segments.

        Returns:
            str: List of [start, intensity] pairs.
        """
        return str(self.segments)
