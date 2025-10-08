# Plotting Helper: `ysy_plot_helper.py`

A lightweight and pragmatic personal Python plotting helper based on Matplotlib.

It provides an "out-of-the-box" standardized plotting function and a composable temporary style loader to help you maintain a consistent and aesthetically pleasing plotting style across Jupyter Notebooks, Python scripts, and academic papers.

## Features

  * **Standardized plotting function `plot(...)`**: Creates common line or scatter plots with a single line of code, including settings for titles, axis labels, legends, and native support for multiple data series.
  * **Temporary style loader `temp_style(...)`**: Utilizes a `with` block to dynamically combine multiple built-in style snippets and your custom configurations into a temporary `.mplstyle` file. This style is active only within the block and automatically reverts to Matplotlib's default settings upon exit, ensuring the global environment is never polluted.
  * **Composable built-in style library `PRESET_STYLES`**: Includes a collection of well-designed style snippets, clearly categorized into "layout" (controlling dimensions, fonts, ticks, etc.) and "color" (controlling palettes, foreground/background colors, etc.), allowing you to mix and match them like building blocks to create the perfect visual style for your needs.
  * **Quick style preview `print_preset_styles()`**: Quickly prints all available preset styles and their recommended combinations to the console for easy reference and selection.

## Installation

To use, simply copy the `ysy_plot_helper.py` file into your project directory.

## Quick Start

Import the script into your project:

```python
# Import ysy_plot_helper.py
import ysy_plot_helper as yph
import numpy as np
import matplotlib.pyplot as plt
```

### 1\. Quick Plotting (`plot`)

`yph.plot()` encapsulates a basic `matplotlib.pyplot` workflow, ideal for rapid data visualization.

```python
# Prepare data
x = np.linspace(0, 2 * np.pi, 200)
y = np.sin(x)

# Plot with a single line of code
yph.plot(x, y, legend_name='sin(x)', plot_title='Sine Wave', x_label='Radian', y_label='Value')
```

### 2\. Temporary Style Loading (`temp_style`)

Using a `with` statement with `yph.temp_style()` ensures that the style is only applied within the code block, leaving other plots unaffected.

```python
# Use the recommended "ysy_academic" + "sky" style within a with block
with yph.temp_style(["ysy_academic", "sky"]):
    # Create your plot here
    fig, ax = plt.subplots()
    ax.plot(x, np.sin(x), label='sin(x)')
    ax.plot(x, np.cos(x), label='cos(x)')
    ax.set_title('Trigonometric Functions')
    ax.set_xlabel('Radian')
    ax.set_ylabel('Value')
    ax.legend()
    plt.show()

# Outside the with block, the Matplotlib style reverts to its previous state
fig, ax = plt.subplots()
ax.plot(x, np.tan(x), label='tan(x)')
ax.set_title('Another Plot with Default Style')
ax.legend()
plt.show()
```

*For more detailed examples, please refer to the `examples.ipynb` file.*

## API Reference

### `yph.plot(...)`

A high-level plotting function for quickly creating single-axis, single-figure line or scatter plots.

```python
plot(
    x,
    y,
    legend_name,
    plot_title='',
    x_label='X',
    y_label='Y',
    plot_type='curve',
    legend_title='',
    data_point=None
)
```

**Parameters:**

  * `x` (array-like): Data for the horizontal axis.
  * `y` (array-like or list/tuple of array-like): Data for the vertical axis. If a list/tuple, multiple series will be plotted.
  * `legend_name` (str or list[str]): Legend name(s), should match the number of series in `y`.
  * `plot_title` (str): The main title of the plot.
  * `x_label` (str): The label for the horizontal axis.
  * `y_label` (str): The label for the vertical axis.
  * `plot_type` (str): The type of plot, either `'curve'` (line plot) or `'scatter'` (scatter plot).
  * `legend_title` (str): The title for the legend.
  * `data_point` (tuple): A tuple in the format `(x0, y0)`. Only effective for single-series plots, used to highlight a specific data point on the graph.

**Returns:**

  * `None`: This function calls `plt.show()` internally to display the figure and does not return any object.

*Note: This function is designed for the most common "single-axis, single-figure" scenarios. For complex layouts (e.g., subplots, twin axes), please use Matplotlib's native API in conjunction with `temp_style(...)` to unify the style.*

### `yph.temp_style(...)`

A context manager for temporarily applying a set of Matplotlib styles within a specific code block.

```python
temp_style(
    style_keys=None,
    extra_style: str = ""
)
```

**Parameters:**

  * `style_keys` (list[str]): A list of preset style names (keys from `PRESET_STYLES`). Styles are applied sequentially in the order they appear in the list.
  * `extra_style` (str): A string containing additional `rcParams` configurations (one per line, e.g., `'figure.dpi: 150'`). These are applied after the `style_keys` styles and have the highest priority.

**Usage:**

  * Must be used with a `with` statement. Upon entering the `with` block, it generates and applies a temporary `.mplstyle` file. Upon exiting the block (either normally or via an exception), it automatically restores the previous style settings and deletes the temporary file.

## Built-in Styles

Below are three recommended style combinations you can use or modify.

### 1\. `"ysy_academic"` + `"sky"`

This combination is designed for academic writing, especially to pair perfectly with my other project, the **Ysy LaTeX template**. The core design principle is that when the generated figure is inserted into a LaTeX document at `0.7\textwidth`, the font size of elements like the title and labels should closely match the document's main body text (around 11pt), and the aspect ratio should be near the golden ratio for optimal visual harmony. The `"sky"` color scheme also originates from the theme of the same name in Ysy LaTeX.

### 2\. `"science"` + `"science_color"`

The inspiration and design of this combination are largely drawn from the excellent `SciencePlots` package, aiming to replicate the plotting style of the top-tier journal *Science*. Its clean, clear, and professional appearance makes it highly suitable for formal scientific publications. It also pairs well with the `Elegant` color theme in the Ysy LaTeX template.

### 3\. `"ieee"` + `"ieee_color"`

> IEEE requires figures to be readable when printed in black and white. The ieee style also sets the figure width to fit within one column of an IEEE paper.

The creation of this style was inspired by a story that moved me:

> While browsing the internet one day, I came across a message that struck me: "Having attended several conferences in Germany, I've seen many retired professors, some so old they are unsteady on their feet, still participating. You can tell they are truly passionate. My former advisor once told me to avoid overly colorful plots in papers and use black and white as much as possible, because some old professors dislike reading on a screen. They prefer to print articles out, and if your plots are too colorful, they can't distinguish the details in a black-and-white printout."

This story is a reminder that academic work should be accessible to all readers, including older generations of scholars who are accustomed to reading black-and-white printouts. The IEEE publication guidelines also explicitly state this requirement. Therefore, I implemented this `ieee` style, referencing `SciencePlots`, which not only optimizes for grayscale readability but also sets the default figure width to fit a single column in a standard two-column IEEE paper.

> "True researchers are pioneers, always venturing into the wilderness."

I hope this small script can offer some convenience on your path of discovery.

## FAQ

**Q: Why does my code raise a color format error (e.g., about hex codes)?**
A: Some preset styles (like Catppuccin) use hex color codes without the `#` prefix (e.g., `89b4fa`). While newer versions of Matplotlib can parse these, some versions or backends may require the standard `#89b4fa` format. If you encounter a color parsing error, please check the `PRESET_STYLES` dictionary in `ysy_plot_helper.py` and add the `#` prefix to the relevant color values.

**Q: Does `temp_style` write files to the system's temporary directory?**
A: Yes. It creates a `.mplstyle` file in the system's temporary directory. This file is automatically deleted when the `with` block exits normally. However, if your Python process is force-killed (e.g., with `kill -9`), this temporary file may remain. These residual files will not affect the script's functionality.

**Q: Why does the `plot` function always call `plt.show()` instead of returning `fig` and `ax` objects?**
A: This function was designed for "quick plotting" in simple data exploration and visualization scenarios. If you need more flexible object-level control (e.g., returning `fig` and `ax` for further customization or saving), we recommend using Matplotlib's native API (like `plt.subplots()`) or copying and slightly modifying the `plot` function's source code to fit your needs.

**Q: How can I customize or add my own styles?**
A: There are two easy ways:

  * **A (Temporary Modification)**: Write your `rcParams` configurations as a multi-line string and pass it through the `extra_style` parameter of `temp_style`. This is the quickest method.
  * **B (Permanent Addition)**: Directly add your new key-value pair to the `PRESET_STYLES` dictionary in the `ysy_plot_helper.py` file. It is recommended to follow the principle of separating "layout" and "color" styles for better reusability.

**Q: How do I configure parameters for saving (exporting) figures?**
A: It's best to configure these parameters within your "layout" styles. Common settings include `savefig.bbox: tight` (to automatically trim whitespace), `savefig.pad_inches: 0.05` (to set padding), and an appropriate `figure.dpi` (e.g., `300`) to ensure high-quality output.

## References and Acknowledgements

The style designs in this script, particularly the `science` and `ieee` styles, are heavily inspired by and reference the [**Science Plots**](https://github.com/garrettj403/SciencePlots) project, which is an excellent Matplotlib style library.

### Citation

If this script is highly beneficial to your academic work, please consider citing the original author's `SciencePlots` package:

```bibtex
@article{SciencePlots,
  author  = {John D. Garrett},
  title   = {{garrettj403/SciencePlots}},
  month   = sep,
  year    = 2021,
  publisher = {Zenodo},
  version = {1.0.9},
  doi     = {10.5281/zenodo.4106649},
  url     = {http://doi.org/10.5281/zenodo.4106649}
}
```

### Acknowledgements

  * The Matplotlib team and its vast community of contributors.
  * The creators of various classic color schemes (e.g., Catppuccin, Nord).
  * All friends who have provided valuable feedback and suggestions for this script.

## License

This project is licensed under the [MIT License](https://www.google.com/search?q=LICENSE). You are free to use, modify, and distribute it.