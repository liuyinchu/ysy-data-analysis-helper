
# 绘图助手 `ysy_plot_helper.py`

一个轻量、务实的个人 Python 绘图助手，基于 Matplotlib。

提供一个“开箱即用”的标准化绘图入口和一个可组合的临时样式加载器，帮助您在 Jupyter Notebook、Python 脚本与学术论文之间保持一致、美观的出图风格。

## ✨ 特性

  * **标准化绘图函数 `plot(...)`**：一行代码完成常见的折线/散点图绘制，包括标题、坐标轴标签、图例等常用元素的设置，并原生支持多数据序列。
  * **临时样式加载器 `temp_style(...)`**：以 `with` 代码块的形式，将多个内置样式片段与您的自定义配置项动态组合成一个临时的 `.mplstyle` 样式文件。该样式仅在代码块内生效，结束后自动恢复 Matplotlib 的默认设置，绝不污染全局环境。
  * **可组合的内置样式库 `PRESET_STYLES`**：内置多套精心设计的样式片段，并清晰地将它们区分为“布局类”（控制尺寸、字体、坐标刻度等）与“配色类”（控制色盘、前景/背景色等），允许您像搭积木一样自由组合，创造出最适合您当前需求的视觉风格。
  * **样式快速预览 `print_preset_styles()`**：在命令行中快速打印出所有可用的预设样式及其推荐组合，方便您随时查阅和选用。

## 📦 安装

将 `ysy_plot_helper.py` 文件复制到您的项目目录中即可使用。

## 🚀 快速开始

将脚本导入您的项目中：

```python
# 导入 ysy_plot_helper.py
import ysy_plot_helper as yph
import numpy as np
import matplotlib.pyplot as plt
```

### 1\. 快速出图 (`plot`)

`yph.plot()` 封装了一个基础的 `matplotlib.pyplot` 绘图流程，特别适合快速可视化数据。

```python
# 准备数据
x = np.linspace(0, 2 * np.pi, 200)
y = np.sin(x)

# 一行代码出图
yph.plot(x, y, legend_name='sin(x)', plot_title='Sine Wave', x_label='Radian', y_label='Value')
```

### 2\. 临时样式加载 (`temp_style`)

使用 `with` 语句和 `yph.temp_style()`，可以保证样式只在代码块内部生效，不影响其他图表。

```python
# 在 with 代码块中使用推荐的 "学术" + "天空蓝" 风格
with yph.temp_style(["ysy_academic", "sky"]):
    # 在这里创建你的图形
    fig, ax = plt.subplots()
    ax.plot(x, np.sin(x), label='sin(x)')
    ax.plot(x, np.cos(x), label='cos(x)')
    ax.set_title('Trigonometric Functions')
    ax.set_xlabel('Radian')
    ax.set_ylabel('Value')
    ax.legend()
    plt.show()

# 在 with 代码块之外，Matplotlib 样式会恢复到之前的状态
fig, ax = plt.subplots()
ax.plot(x, np.tan(x), label='tan(x)')
ax.set_title('Another Plot with Default Style')
ax.legend()
plt.show()
```

*更多详细用法请参考 `examples.ipynb` 文件。*

## 📚 API 参考

### `yph.plot(...)`

一个高级绘图函数，用于快速创建单轴、单图的折线图或散点图。

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

**参数说明：**

  * `x` (array-like): 横轴数据。
  * `y` (array-like or list/tuple of array-like): 纵轴数据。若为列表/元组，则绘制多条序列。
  * `legend_name` (str or list[str]): 图例名称，应与 `y` 的序列数量匹配。
  * `plot_title` (str): 图表主标题。
  * `x_label` (str): 横轴标签。
  * `y_label` (str): 纵轴标签。
  * `plot_type` (str): 绘图类型，可选 `'curve'` (折线图) 或 `'scatter'` (散点图)。
  * `legend_title` (str): 图例的标题。
  * `data_point` (tuple): 格式为 `(x0, y0)`。仅在单序列绘图时生效，用于高亮标记图上的一个特定数据点。

**返回：**

  * `None`: 该函数内部直接调用 `plt.show()` 来显示图像，不返回任何对象。

*注意：此函数旨在处理最常见的“单轴单图”场景。对于复杂布局（如多子图、双Y轴等），请直接使用 Matplotlib 的原生 API，并搭配 `temp_style(...)` 来统一风格。*

### `yph.temp_style(...)`

一个上下文管理器，用于在特定的代码块内临时应用一组 Matplotlib 样式。

```python
temp_style(
    style_keys=None,
    extra_style: str = ""
)
```

**参数说明：**

  * `style_keys` (list[str]): 一个包含预设样式名称（`PRESET_STYLES` 中的键）的列表。样式会按照列表中的顺序依次叠加生效。
  * `extra_style` (str): 一个包含额外 `rcParams` 配置的字符串（每行一个配置，例如 `'figure.dpi: 150'`）。这些配置会追加在 `style_keys` 定义的样式之后，拥有最高优先级。

**用法：**

  * 必须与 `with` 语句一同使用。进入 `with` 块时，它会自动生成一个临时的 `.mplstyle` 文件并应用该样式；退出 `with` 块时（无论正常退出还是发生异常），它都会自动恢复之前的样式设置并删除临时文件。

## 🎨 内置样式介绍

以下是三种推荐的样式组合，您可以根据需求选用或进行修改。

### 1\. `"ysy_academic"` + `"sky"`

这套组合是为学术写作而设计的，特别是为了与我的另一个项目 **Ysy LaTeX 模板** 完美配合。
设计的核心理念是：当生成的图片以 `0.7\textwidth` 的宽度插入 LaTeX 文档时，图中的文字大小（如标题、标签）应与文章的正文字号（约 11pt）基本一致，且图片的宽高比接近黄金比例，以获得最佳的视觉协调性。`"sky"` 配色方案同样源自 Ysy LaTeX 中的同名主题。

### 2\. `"science"` + `"science_color"`

这套组合的灵感与设计绝大部分来自于优秀的 `SciencePlots` 包，旨在复现顶级期刊 *Science* 的绘图风格。其简洁、清晰、专业的视觉呈现使其非常适用于正式的科学出版物。特别地，它与 Ysy LaTeX 模板中的 `Elegant` 配色主题也十分搭调。

### 3\. `"ieee"` + `"ieee_color"`

>IEEE requires figures to be readable when printed in black and white. The ieee style also sets the figure width to fit within one column of an IEEE paper.

这套样式的诞生源于一个触动我的故事：

> 某天网上冲浪，看到这样一条消息，颇有感触：“在德国参加几次会议，真的会见到好几个那种路都走不稳，退休好多年的老教授还去参加会议，真的觉得他们是真热爱。之前外导还嘱咐我，文章里的图颜色别花花绿绿的，尽量用黑白，因为会有老教授不喜欢读电子版的，他们喜欢打印出来读，如果你文章里全是花花绿绿的，他们打印下来也分辨不清。”

这个故事提醒我们，学术成果的传播应当考虑到所有读者，包括那些习惯于阅读黑白打印稿的老一辈学者。IEEE 的出版规范也明确要求：“图形在黑白打印时必须是可读的”。因此，我参考 `SciencePlots` 实现了这套 `ieee` 样式，它不仅优化了灰度可读性，还将图形宽度默认设置为适合 IEEE 双栏论文的单栏宽度。

> “真正的科研工作者总是前赴后继地奔赴那片荒原。”

希望这份小小的脚本，能为您的探索之路提供些许便利。

## ❓ 常见问题 (FAQ)

**Q: 为什么我的代码会报颜色格式错误（例如，关于 hex 码）？**
A: 部分预设样式（如 Catppuccin）使用了不带 `#` 前缀的十六进制颜色码（例如 `89b4fa`）。虽然较新版本的 Matplotlib 能够解析它们，但部分版本或后端可能需要 `#89b4fa` 这种标准格式。如果您遇到颜色解析错误，请检查 `ysy_plot_helper.py` 中的 `PRESET_STYLES` 字典，并为相关的色值批量补上 `#` 前缀。

**Q: `temp_style` 会在系统临时目录中写入文件吗？**
A: 会的。它会在系统的临时目录中创建一个 `.mplstyle` 文件。当 `with` 块正常退出时，该文件会被自动删除。但如果您的 Python 进程被强制终止（例如 `kill -9`），这个临时文件可能会残留下来。不过，残留的文件不会影响脚本的正常功能。

**Q: `plot` 函数为什么总是调用 `plt.show()`，而不是返回 `fig` 和 `ax` 对象？**
A: 这个函数的设计初衷是“快速出图”，用于简单的数据探索和可视化场景。如果您需要更灵活的对象级控制（例如，返回 `fig`, `ax` 对象以便进行更复杂的定制或保存），我们建议您直接使用 Matplotlib 的原生 API（如 `plt.subplots()`），或者根据您的需求，拷贝并微调 `plot` 函数的源码。

**Q: 我该如何自定义或添加我自己的样式？**
A: 有两种便捷的方式：

  * **方式 A (临时修改)**：将您的 `rcParams` 配置写成一个多行字符串，然后通过 `temp_style` 的 `extra_style` 参数传入。这是最快的方式。
  * **方式 B (永久添加)**：直接在 `ysy_plot_helper.py` 文件的 `PRESET_STYLES` 字典中新增您的键值对。建议遵循“布局”与“配色”分离的原则来组织您的样式，以便更好地复用。

**Q: 如何配置保存图片（导出）时的参数？**
A: 建议将这些参数配置在您的“布局类”样式中。常用的配置项包括：`savefig.bbox: tight` (自动裁剪白边), `savefig.pad_inches: 0.05` (设置边距), 以及设置一个合适的 `figure.dpi` (例如 `300`) 来保证导出图像的清晰度。

## 📜 参考与致谢

本脚本的样式设计，特别是 `science` 和 `ieee` 风格，大量参考了 [**Science Plots**](https://github.com/garrettj403/SciencePlots) 项目。它是一个非常出色的 Matplotlib 样式库。

### 引用

如果这个脚本对您的学术工作非常有帮助，希望您能考虑引用原作者的 `SciencePlots` 包：

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

### 致谢

  * Matplotlib 团队与广大的社区贡献者。
  * 各经典配色方案（如 Catppuccin, Nord 等）的创作者。
  * 所有为这个脚本提出宝贵反馈与建议的朋友们。

## 📄 许可

本项目采用 [MIT License](https://www.google.com/search?q=LICENSE)。您可以自由地使用、修改与分发。