# IntensitySegments

A Python module to manage and update intensity values across continuous segments on the real number line.

The module supports three main operations:
- **add(from, to, amount)**: Adds an amount to the intensity within a specified range `[from, to)`.
- **set(from, to, amount)**: Sets the intensity to a specific value within a specified range `[from, to)`.
- **__str__()**: Returns a compact string representation of the segments.

---

## Requirements

- Python 3.8 or higher
- pytest (for running tests)

Make sure you have Python 3.8+ installed.  
You can download Python from: https://www.python.org/

---

## Usage Example

```python
from intensity_segments.intensity_segments import IntensitySegments

segments = IntensitySegments()
print(segments)  # Output: []

segments.add(10, 30, 1)
print(segments)  # Output: [[10, 1], [30, 0]]

segments.add(20, 40, 1)
print(segments)  # Output: [[10, 1], [20, 2], [30, 1], [40, 0]]

segments.add(10, 40, -2)
print(segments)  # Output: [[10, -1], [20, 0], [30, -1], [40, 0]]
```

---

## Running Tests

Tests are written using `pytest`.

To run all tests:

```bash
pytest ./intensity_segments/
```

The tests cover:
- Basic operations (add, set).
- Mixed sequences of operations.
- Handling of empty or invalid ranges.
- Merging of adjacent segments with the same intensity.

---

## Notes

- All intensity values start from 0.
- The implementation automatically merges adjacent segments with identical intensity values for compactness.
- Empty or invalid ranges (where `from_ >= to`) are ignored safely.

---

## License

This project is licensed under the MIT License.

---

## Author

Nian Li
