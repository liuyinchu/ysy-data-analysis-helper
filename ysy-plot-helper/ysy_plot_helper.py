"""
ysy_plot_helper.py

Copyright (c) 2025 pifuyuini

Author: pifuyuini
Email: You can contact me via Github
Version: 1.6.0
Date: 2025-09-06

Description
-----------
A tiny, pragmatic plotting helper focused on two things:
1) a simple, standardized plotting function (`plot`) for quick curves/scatters, and
2) a lightweight style manager (`temp_style`) that temporarily assembles and applies
   Matplotlib `.mplstyle` snippets (from built-in presets plus optional overrides).

This module is intentionally minimal. It is *not* a full plotting library—just a
thin layer to speed up everyday plotting and keep style usage consistent across
notebooks, scripts, and papers.

Key Features
------------
- `plot(...)`: one-call line/scatter plotting with sensible defaults and legend/title.
- `temp_style(style_keys, extra_style)`: context manager that composes a temporary
  `.mplstyle` file from selected presets and/or extra rcParams, applies it inside
  the `with` block, and then cleanly restores Matplotlib defaults.
- `print_preset_styles()`: quick guide to available layout and color theme presets.
- `PRESET_STYLES`: a dictionary of small, focused `.mplstyle` fragments. You can mix
  “layout” presets (sizes, ticks, fonts, legends, etc.) with “color” presets.

Usage
-----
Quick start for plotting:
    >>> from ysy_plot_helper import plot
    >>> import numpy as np
    >>> x = np.linspace(0, 2*np.pi, 200)
    >>> y = np.sin(x)
    >>> plot(x, y, legend_name='sin(x)', plot_title='Sine', x_label='x', y_label='y')

Using temporary styles:
    >>> from ysy_plot_helper import temp_style, plot, print_preset_styles
    >>> print_preset_styles()  # inspect available presets
    >>> with temp_style(['ysy_academic', 'sky']):  # layout + color
    ...     plot(x, y, legend_name='sin(x)', plot_title='Styled Sine')

Composing with overrides:
    >>> extra = "lines.linewidth: 2.5\naxes.grid: True\n"
    >>> with temp_style(['science'], extra_style=extra):
    ...     plot(x, y, legend_name='sin(x)')

Notes & Limitations
-------------------
- Hex colors in `.mplstyle` usually require a leading '#'. Several presets below
  use bare hex strings (e.g., '89b4fa'). If Matplotlib throws a parsing error on
  your setup, prefix them with '#'.
- The style manager writes a temporary `.mplstyle` file and removes it on exit.
  If your program is interrupted mid-block, the file may linger in temp space.
- `plot` is intentionally simple. For complex layouts (subplots, twin axes,
  secondary scales, etc.), call Matplotlib directly and optionally wrap with
  `temp_style(...)`.

License
-------
MIT

Changelog
---------
v1.6.0: Refactor script, remove unnecessary pieces, add IEEE theme.
"""

__version__ = "1.6.0"

# Import necessary packages
import matplotlib.pyplot as plt
from cycler import cycler
from matplotlib.colors import LinearSegmentedColormap  # Reserved for future custom colormaps
import matplotlib.style as mplstyle
import tempfile, os, contextlib


# =========================
# Plot
# =========================

def plot(
    x,
    y,
    legend_name,
    plot_title: str = '',
    x_label: str = 'X',
    y_label: str = 'Y',
    plot_type: str = 'curve',
    legend_title: str = '',
    data_point=None,
):
    """
    Create a quick standardized plot (line or scatter) with minimal boilerplate.

    Parameters
    ----------
    x : array-like
        X-axis data.

    y : array-like or list/tuple of array-like
        Y-axis data. If `y` is a list/tuple, each element is plotted as a separate series.

    legend_name : str or list[str]
        Legend label for the series. If `y` is a list/tuple, `legend_name` should be a
        list of equal length providing a label for each series.

    plot_title : str, optional
        Figure title.

    x_label : str, optional
        X-axis label (default 'X').

    y_label : str, optional
        Y-axis label (default 'Y').

    plot_type : {'curve', 'scatter'}, optional
        Plot as continuous lines ('curve') or points ('scatter'). Default 'curve'.

    legend_title : str, optional
        Title for the legend box (empty by default).

    data_point : tuple[float, float] | None, optional
        If provided *and* `y` is a single series, highlight one specific data point as
        an 'x' marker (zorder=2) on top of the line. Example: (x0, y0).

    Returns
    -------
    None
        Displays the plot via `plt.show()`.

    Examples
    --------
    Single series:
        >>> plot(x, y, legend_name='sin', plot_title='Sine', x_label='x', y_label='y')

    Multiple series:
        >>> y2 = np.cos(x)
        >>> plot(x, [y, y2], legend_name=['sin', 'cos'], plot_title='Trigs')

    Notes
    -----
    - This helper uses a single Axes and calls `plt.show()` immediately.
    - For complex layouts, call Matplotlib directly or extend this function.
    """
    plt.figure()

    # Support plotting multiple series when y is a list/tuple.
    if isinstance(y, tuple) or isinstance(y, list):
        for i in range(len(y)):
            if plot_type == 'curve':
                plt.plot(x, y[i], label=legend_name[i])
            elif plot_type == 'scatter':
                plt.scatter(x, y[i], label=legend_name[i])
    else:
        # Single series branch.
        if plot_type == 'curve':
            plt.plot(x, y, label=legend_name, zorder=1)
            if data_point is not None:
                # Highlight an individual point on top of the line.
                plt.scatter(
                    data_point[0],
                    data_point[1],
                    label='Data Point',
                    color='C1',
                    marker='x',
                    zorder=2,
                )
        elif plot_type == 'scatter':
            plt.scatter(x, y, label=legend_name)

    # Standard labels/legend/title.
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(plot_title)
    plt.legend(title=legend_title)
    plt.show()
    return None


# =========================
# Style Manager
# =========================

@contextlib.contextmanager
def temp_style(style_keys=None, extra_style: str = ""):
    """
    Temporarily apply a composed Matplotlib style built from preset snippets and/or
    an additional inline style string.

    This context manager:
    1) concatenates the requested presets in order,
    2) appends any `extra_style` rcParams lines,
    3) writes them to a temporary `.mplstyle`,
    4) applies it via `matplotlib.style.use`,
    5) restores the default style and removes the temp file on exit.

    Parameters
    ----------
    style_keys : list[str] | None, optional
        Keys into `PRESET_STYLES`. Presets are concatenated in the given order.
        If None, only `extra_style` is used.

    extra_style : str, optional
        Additional `.mplstyle` content (raw rcParams lines), appended after presets.
        Example:
            "lines.linewidth: 2.0\\naxes.grid: True\\n"

    Yields
    ------
    None
        Use inside a `with` block. All plotting within the block uses the composed style.

    Raises
    ------
    ValueError
        If any key in `style_keys` is not defined in `PRESET_STYLES`.

    Examples
    --------
    Combine layout + color theme:
        >>> with temp_style(['ysy_academic', 'sky']):
        ...     plot(x, y, legend_name='Series A')

    Add inline overrides:
        >>> extra = "legend.frameon: False\\nlines.markersize: 4\\n"
        >>> with temp_style(['science'], extra_style=extra):
        ...     plot(x, y, legend_name='Series B')

    Notes
    -----
    - If your process is killed inside the context, the temporary .mplstyle file may remain
      in the temp directory. It is removed on normal exit.
    - Preset fragments are short by design; mix “layout” and “color” layers as needed.
    """
    combined_style = ""
    if style_keys:
        for key in style_keys:
            if key in PRESET_STYLES:
                combined_style += PRESET_STYLES[key] + "\n"
            else:
                raise ValueError(f"Unknown style key: {key}")
    combined_style += extra_style

    # Write the composed style to a temporary .mplstyle file.
    with tempfile.NamedTemporaryFile('w+', suffix='.mplstyle', delete=False) as tmp:
        tmp.write(combined_style)
        tmp_path = tmp.name

    try:
        # Apply the temporary style.
        mplstyle.use(tmp_path)
        yield
    finally:
        # Always restore defaults and clean up the temp file.
        mplstyle.reload_library()
        mplstyle.use('default')
        os.remove(tmp_path)


def print_preset_styles():
    """
    Print a short guide to recommended style-loading patterns and available presets.

    This is a convenience inspector—useful for quick discovery at the REPL/Jupyter.
    """
    print('=== Recommended Loading Format ===')
    print('with yph.temp_style(["ysy_academic", "sky"]):')
    print()
    print('=== Drawing Layout ===')
    print("ysy_common, ysy_jupyter, sci_common, science (recommended), "
          "ysy_academic (recommended), ieee (recommended)")
    print()
    print('=== Color Themes ===')
    print(
        '''catppuccin_mocha (dark, recommended),
catppuccin_latte (recommended),
ysy_firefly_1 (lightweight),
science_color (lightweight),
catppuccin_farppe (dark),
nord_light,
nord_dark (dark),
school_light (lightweight),
sky (lightweight, recommended),
ysy_firefly_2 (grayscale, lightweight),
cold_nature (lightweight),
mondrian_dunghuang (lightweight),
sky2 (lightweight),
ieee_color (lightweight)
'''
    )
    return None


# =========================
# Preset Styles (rcParams fragments)
# =========================
PRESET_STYLES = {
    # -------- Layout presets --------
    "ysy_common": """
figure.figsize         : 12.5, 9
figure.dpi             : 300

axes.labelsize         : 27
axes.titlesize         : 30

xtick.major.size       : 9
xtick.major.width      : 1.5
xtick.minor.size       : 4.5
xtick.minor.width      : 1.5

ytick.major.size       : 9
ytick.major.width      : 1.5
ytick.minor.size       : 4.5
ytick.minor.width      : 1.5

xtick.labelsize        : 25
ytick.labelsize        : 25

axes.grid              : True
axes.axisbelow         : True
grid.linestyle         : --
grid.alpha             : 0.75
grid.linewidth         : 1

legend.frameon         : True
legend.framealpha      : 1.0
legend.fancybox        : True
legend.numpoints       : 1
legend.shadow          : True
legend.fontsize        : 25
legend.title_fontsize  : 25

lines.linewidth        : 3.0

# Font settings
font.family            : serif
font.serif             : cmr10, Computer Modern Serif, DejaVu Serif
axes.formatter.use_mathtext : True
mathtext.fontset       : cm
text.usetex            : False
""",

    "ysy_jupyter": """
figure.figsize         : 8, 6
figure.dpi             : 300

axes.labelsize         : 16
axes.titlesize         : 16
axes.linewidth         : 1

xtick.major.size       : 6
xtick.major.width      : 1
xtick.minor.size       : 3
xtick.minor.width      : 1
xtick.labelsize        : 16

ytick.major.size       : 6
ytick.major.width      : 1
ytick.minor.size       : 3
ytick.minor.width      : 1
ytick.labelsize        : 16

axes.grid              : True
axes.axisbelow         : True
grid.linestyle         : --
grid.alpha             : 0.75
grid.linewidth         : 1

legend.frameon         : True
legend.framealpha      : 1.0
legend.fancybox        : True
legend.numpoints       : 1
legend.shadow          : True
legend.fontsize        : 16
legend.title_fontsize  : 16

lines.linewidth        : 2.0

font.family            : sans-serif
mathtext.fontset       : dejavusans
text.usetex            : False
""",

    "sci_common": """
figure.figsize        : 3.375, 2.5
figure.dpi            : 300
savefig.dpi           : 300

font.family           : serif
font.size             : 8
axes.labelsize        : 8
axes.titlesize        : 8
xtick.labelsize       : 7
ytick.labelsize       : 7
legend.fontsize       : 7

lines.linewidth       : 1
lines.markersize      : 3

axes.linewidth        : 0.5
xtick.major.size      : 3
xtick.major.width     : 0.5
ytick.major.size      : 3
ytick.major.width     : 0.5

axes.grid             : False
legend.frameon        : False
pdf.fonttype          : 42
ps.fonttype           : 42
text.usetex           : False
""",

    "science": """
figure.figsize           : 3.5, 2.625

xtick.direction          : in
xtick.major.size         : 3
xtick.major.width        : 0.5
xtick.minor.size         : 1.5
xtick.minor.width        : 0.5
xtick.minor.visible      : True
xtick.top                : True

ytick.direction          : in
ytick.major.size         : 3
ytick.major.width        : 0.5
ytick.minor.size         : 1.5
ytick.minor.width        : 0.5
ytick.minor.visible      : True
ytick.right              : True

axes.linewidth           : 0.5
grid.linewidth           : 0.5
lines.linewidth          : 1.0

legend.frameon           : False
savefig.bbox             : tight
savefig.pad_inches       : 0.05

font.family              : serif
mathtext.fontset         : dejavuserif
""",

    "ysy_academic": """
figure.figsize         : 4.7, 2.9
figure.dpi             : 300

axes.labelsize         : 10.5
axes.titlesize         : 11.5
axes.linewidth         : 0.75

xtick.major.size       : 3
xtick.major.width      : 0.75
xtick.minor.size       : 1.5
xtick.minor.width      : 0.5
xtick.minor.visible    : False
xtick.top              : False

ytick.major.size       : 3
ytick.major.width      : 0.75
ytick.minor.size       : 1.5
ytick.minor.width      : 0.5
ytick.minor.visible    : False
ytick.right            : False

xtick.labelsize        : 9.5
ytick.labelsize        : 9.5

axes.grid              : False
axes.axisbelow         : True
grid.linestyle         : --
grid.alpha             : 0.85
grid.linewidth         : 0.75

legend.frameon         : True
legend.framealpha      : 1
legend.fancybox        : True
legend.numpoints       : 1
legend.shadow          : False
legend.fontsize        : 10
legend.title_fontsize  : 10

lines.linewidth        : 1.5
lines.markersize       : 5

# Font settings
font.family            : serif
axes.formatter.use_mathtext : True
mathtext.fontset       : cm
text.usetex            : False
""",

    "ieee": """
# IEEE-like compact layout for small figures.
figure.figsize : 3.3, 2.5
figure.dpi : 600

font.size : 8
font.family : serif
font.serif : Times

xtick.direction          : in
xtick.major.size         : 3
xtick.major.width        : 0.5
xtick.minor.size         : 1.5
xtick.minor.width        : 0.5
xtick.minor.visible      : True
xtick.top                : True

ytick.direction          : in
ytick.major.size         : 3
ytick.major.width        : 0.5
ytick.minor.size         : 1.5
ytick.minor.width        : 0.5
ytick.minor.visible      : True
ytick.right              : True

axes.linewidth           : 0.5
grid.linewidth           : 0.5
lines.linewidth          : 1.0

legend.frameon           : False
savefig.bbox             : tight
savefig.pad_inches       : 0.05
""",

    # -------- Color/theme presets --------
    "catppuccin_mocha": """
# Catppuccin Mocha color theme (dark UI style)
axes.prop_cycle: cycler('color', ['89b4fa', 'fab387', 'a6e3a1', 'f38ba8', 'cba6f7', 'eba0ac', 'f5c2e7', 'f5e0dc', '94e2d5', 'b4befe'])

# Font color: Text
text.color: cdd6f4
axes.labelcolor: cdd6f4
xtick.labelcolor: cdd6f4
ytick.labelcolor: cdd6f4

# Background color: Base
figure.facecolor: 1e1e2e
axes.facecolor: 1e1e2e
savefig.facecolor: 1e1e2e

# Edge color: Surface 0
axes.edgecolor: 313244
legend.edgecolor: 313244
xtick.color: 313244
ytick.color: 313244
patch.edgecolor: 313244
hatch.color: 313244

# Grid color: Surface 0
grid.color: 313244

# Boxplots
boxplot.flierprops.color: 6c7086
boxplot.flierprops.markerfacecolor: 6c7086
boxplot.flierprops.markeredgecolor: 6c7086
boxplot.boxprops.color: 6c7086
boxplot.whiskerprops.color: 6c7086
boxplot.capprops.color: 6c7086
boxplot.medianprops.color: 6c7086
boxplot.meanprops.color: 6c7086
boxplot.meanprops.markerfacecolor: 6c7086
boxplot.meanprops.markeredgecolor: 6c7086
""",

    "catppuccin_latte": """
# Light variant of Catppuccin.
axes.prop_cycle: cycler('color', ['1e66f5', 'fe640b', '40a02b', 'd20f39', '8839ef', 'e64553', 'ea76cb', 'dc8a78', '179299', '7287fd'])

text.color: 4c4f69
axes.labelcolor: 4c4f69
xtick.labelcolor: 4c4f69
ytick.labelcolor: 4c4f69

figure.facecolor: eff1f5
axes.facecolor: eff1f5
savefig.facecolor: eff1f5

axes.edgecolor: ccd0da
legend.edgecolor: ccd0da
xtick.color: ccd0da
ytick.color: ccd0da
patch.edgecolor: ccd0da
hatch.color: ccd0da

grid.color: ccd0da

# Boxplots
boxplot.flierprops.color: 9ca0b0
boxplot.flierprops.markerfacecolor: 9ca0b0
boxplot.flierprops.markeredgecolor: 9ca0b0
boxplot.boxprops.color: 9ca0b0
boxplot.whiskerprops.color: 9ca0b0
boxplot.capprops.color: 9ca0b0
boxplot.medianprops.color: 9ca0b0
boxplot.meanprops.color: 9ca0b0
boxplot.meanprops.markerfacecolor: 9ca0b0
boxplot.meanprops.markeredgecolor: 9ca0b0
""",

    "ysy_firefly_1": """
axes.prop_cycle : cycler('color', ['475d7b', '97c6c0', 'e26e1b', '4df8e8', '3e324a', '6b8fb4', 'f1b349', 'a081af'])
grid.color: k
""",

    "science_color": """
axes.prop_cycle : cycler('color', ['0C5DA5', '00B945', 'FF9500', 'FF2C00', '845B97', '474747', '9e9e9e'])
grid.color: k
""",

    "catppuccin_farppe": """
axes.prop_cycle: cycler('color', ['8caaee', 'ef9f76', 'a6d189', 'e78284', 'ca9ee6', 'ea999c', 'f4b8e4', 'f2d5cf', '81c8be', 'babbf1'])

text.color: c6d0f5
axes.labelcolor: c6d0f5
xtick.labelcolor: c6d0f5
ytick.labelcolor: c6d0f5

figure.facecolor: 303446
axes.facecolor: 303446
savefig.facecolor: 303446

axes.edgecolor: 414559
legend.edgecolor: 414559
xtick.color: 414559
ytick.color: 414559
patch.edgecolor: 414559
hatch.color: 414559

grid.color: 414559

# Boxplots
boxplot.flierprops.color: 737994
boxplot.flierprops.markerfacecolor: 737994
boxplot.flierprops.markeredgecolor: 737994
boxplot.boxprops.color: 737994
boxplot.whiskerprops.color: 737994
boxplot.capprops.color: 737994
boxplot.medianprops.color: 737994
boxplot.meanprops.color: 737994
boxplot.meanprops.markerfacecolor: 737994
boxplot.meanprops.markeredgecolor: 737994
""",

    "nord_light": """
axes.prop_cycle: cycler('color', ['5e81ac', '88c0d0', 'a3be8c', 'd08770', 'bf616a', 'b48ead', 'ebcb8b', '81a1c1', '8fbcbb', '4c566a'])

text.color: 2e3440
axes.labelcolor: 2e3440
xtick.labelcolor: 2e3440
ytick.labelcolor: 2e3440

figure.facecolor: eceff4
axes.facecolor: eceff4
savefig.facecolor: eceff4

axes.edgecolor: d8dee9
legend.edgecolor: d8dee9
xtick.color: d8dee9
ytick.color: d8dee9
patch.edgecolor: d8dee9
hatch.color: d8dee9

grid.color: d8dee9

# Boxplots
boxplot.flierprops.color: 4c566a
boxplot.flierprops.markerfacecolor: 4c566a
boxplot.flierprops.markeredgecolor: 4c566a
boxplot.boxprops.color: 4c566a
boxplot.whiskerprops.color: 4c566a
boxplot.capprops.color: 4c566a
boxplot.medianprops.color: 4c566a
boxplot.meanprops.color: 4c566a
boxplot.meanprops.markerfacecolor: 4c566a
boxplot.meanprops.markeredgecolor: 4c566a
""",

    "nord_dark": """
axes.prop_cycle: cycler('color', ['81a1c1', '8fbcbb', 'a3be8c', 'b48ead', 'd08770', 'bf616a', '5e81ac', '88c0d0', 'ebcb8b', 'eceff4'])

text.color: d8dee9
axes.labelcolor: d8dee9
xtick.labelcolor: d8dee9
ytick.labelcolor: d8dee9

figure.facecolor: 2e3440
axes.facecolor: 2e3440
savefig.facecolor: 2e3440

axes.edgecolor: 4c566a
legend.edgecolor: 4c566a
xtick.color: 4c566a
ytick.color: 4c566a
patch.edgecolor: 4c566a
hatch.color: 4c566a

grid.color: 4c566a

# Boxplots
boxplot.flierprops.color: 616e88
boxplot.flierprops.markerfacecolor: 616e88
boxplot.flierprops.markeredgecolor: 616e88
boxplot.boxprops.color: 616e88
boxplot.whiskerprops.color: 616e88
boxplot.capprops.color: 616e88
boxplot.medianprops.color: 616e88
boxplot.meanprops.color: 616e88
boxplot.meanprops.markerfacecolor: 616e88
boxplot.meanprops.markeredgecolor: 616e88
""",

    "school_light": """
# Elegant light-colored UI theme based on gray-blue and rose accents.
axes.prop_cycle: cycler('color', ['3e324a', '5a6b84', '1c2f62', 'a52a2a', 'd94352', 'c0e4d0', 'bcc7d6'])
""",

    "sky": """
# Sky color theme, based on SkyRelax.
axes.prop_cycle: cycler('color', ['4c55bc', 'ffbe98', 'fc8f9b', 'ad69a2', 'f39477', 'eca4b8', '8c9cc1', 'c8ead4', '63d7fe', '388ef7', 'f7786b', '91dce8', 'd16d7c', '766c9b', '53181f', 'f7b9c2', '555d8b'])
""",

    "ysy_firefly_2": """
# Grayscale-leaning teal sequence for light UIs.
axes.prop_cycle: cycler('color', ['3e5754', '567e79', '6e9f99', '85b6b1', '97c6c0', 'a7d1cb', 'bedfd8', 'd3eae5', 'e8f4f2', 'f5faf9'])
""",

    "cold_nature": """
# Natural dusk palette for light UIs (mixed with Memphis color)
axes.prop_cycle: cycler('color', ['403990', '80A6E2', 'FBDD85', 'F46F43', 'CF3D3E', '077ABD', 'B7AACB', 'F77A82', '89D0C2', 'EFD55E'])
""",

    "mondrian_dunghuang": """
# Bold primaries + earth tones.
axes.prop_cycle: cycler('color', ['0000ff', 'a64c3b', '8fbfb0', 'f20d0d', '6b3b32', 'b78f68', 'cabeaf', '25d4d0', 'ffff00'])
""",

    "sky2": """
# Additional sky theme variant.
axes.prop_cycle: cycler('color', ['388ef7', 'f7786b', '91dce8', 'd16d7c', '766c9b', '53181f', 'f7b9c2', '555d8b'])
""",

    "ieee_color": """
# Simple IEEE-like color+linestyle cycler. Pairs with 'ieee' layout.
axes.prop_cycle : (cycler('color', ['k', 'r', 'b', 'g']) + cycler('ls', ['-', '--', ':', '-.']))
""",
}
