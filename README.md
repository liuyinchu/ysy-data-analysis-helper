# ysy-data-analysis-helper
A Personal Data Analysis Utils Group.

---

Tiny, pragmatic helpers for day-to-day data analysis.  
**First module**: `ysy_plot_helper` — a minimal layer over Matplotlib that gives you:
- `plot(...)`: one-call curve/scatter plotting with sensible defaults.
- `temp_style(style_keys, extra_style)`: compose & apply temporary `.mplstyle` snippets.
- `print_preset_styles()`: list available layout/color presets.

> **Scope**: This is *not* a full plotting library. It’s a thin utility to speed up routine plots and keep style usage consistent across notebooks, scripts, and papers.

---

## Requirements
- Python ≥ 3.11
- matplotlib ≥ 3.7

---

## Install (classmates only; no PyPI)
### Option A — wheel
```bash
pip install ysy_data_analysis_helper-<VERSION>-py3-none-any.whl
```

### Option B — GitHub repo (recommended)

```bash
pip install https://raw.githubusercontent.com/liuyinchu/ysy-data-analysis-helper/main/artifacts/ysy_data_analysis_helper-1.6.0-py3-none-any.whl

```

---

## Quickstart

```python
import numpy as np
from ysy_data_analysis_helper.ysy_plot_helper import plot, temp_style, print_preset_styles

# Data
x = np.linspace(0, 2*np.pi, 300)
y = np.sin(x)

# Basic plot
plot(x, y, legend_name='sin(x)', plot_title='Sine', x_label='x', y_label='y')

# See available presets
print_preset_styles()

# Temporary style: layout+color presets + extra overrides
extra = "lines.linewidth: 2.5\naxes.grid: True\naxes.grid.which: both\n"
with temp_style(['ysy_academic', 'sky'], extra_style=extra):
    plot(x, y, legend_name='styled sin(x)', plot_title='Styled Sine')
```

## If you are the old user of `ysy_plot_helper.py`

**Just make one difference: `import ysy_data_analysis_helper.ysy_plot_helper as yph`. The rest are all the same.**

---

## Versioning

* The package version is defined **inside** `src/ysy_data_analysis_helper/ysy_plot_helper.py` as `__version__`.
* The top-level package exposes the same version via:

  ```python
  import ysy_data_analysis_helper as y
  print(y.__version__)
  ```

---

## License

MIT © pifuyuini