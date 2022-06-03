import configparser

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from basic_functions import closest_string
from curve_fit import fit_data

COLORS = ['red', 'blue', 'green', 'tab:blue', 'tab:orange', 'tab:purple',
          'tab:brown', 'tab:pink', 'tab:olive', 'tab:cyan', 'tab:green']

LINETYPE = ['-', '--', 'o']

MARKERS = ['.',  # point marker
           ',',  # pixel marker
           'o',  # circle marker
           'v',  # triangle_down marker
           '^',  # triangle_up marker
           '<',  # triangle_left marker
           '>',  # triangle_right marker
           '1',  # tri_down marker
           '2',  # tri_up marker
           '3',  # tri_left marker
           '4',  # tri_right marker
           's',  # square marker
           'p',  # pentagon marker
           '*',  # star marker
           'h',  # hexagon1 marker
           'H',  # hexagon2 marker
           '+',  # plus marker
           'x',  # x marker
           'D',  # diamond marker
           'd',  # thin_diamond marker
           '|',  # vline marker
           '_'   # hline marker
           ]

try:
    mpl_config = configparser.ConfigParser()
    with open('matplotlib_config.ini') as config_file:
        mpl_config.read_file(config_file)

    # ----- Figure Size -----
    FIGWIDTH = mpl_config['DEFAULT'].getint('FIGWIDTH')
    FIGHEIGHT = mpl_config['DEFAULT'].getint('FIGHEIGHT')
    # ----- Default Values -----
    DEFAULT_FONT = eval(mpl_config['DEFAULT'].get('DEFAULT_FONT'))
    DEFAULT_COLOR = mpl_config['DEFAULT'].get('DEFAULT_COLOR')
    # ----- Font Values -----
    VERY_SMALL_FONT_SIZE = mpl_config['DEFAULT'].getint('VERY_SMALL_FONT_SIZE')
    SMALL_FONT_SIZE = mpl_config['DEFAULT'].getint('SMALL_FONT_SIZE')
    MEDIUM_FONT_SIZE = mpl_config['DEFAULT'].getint('MEDIUM_FONT_SIZE')
    BIG_FONT_SIZE = mpl_config['DEFAULT'].getint('BIG_FONT_SIZE')
    # ----- Graph Values -----
    CURVE_LINEWIDTH = mpl_config['DEFAULT'].getint('CURVE_LINEWIDTH')
    # ----- Axes Values -----
    AXES_LINEWIDTH = mpl_config['DEFAULT'].getint('AXES_LINEWIDTH')
    # ----- Ticks Values -----
    TICKS_LINEWIDTH = mpl_config['DEFAULT'].getint('TICKS_LINEWIDTH')
    TICKS_LENGTH = mpl_config['DEFAULT'].getint('TICKS_LENGTH')
    GRID = mpl_config['DEFAULT'].getboolean('GRID')

    plt.rc('font', **DEFAULT_FONT)
    # fontsize of the figure title
    plt.rc('figure', titlesize=BIG_FONT_SIZE)
    plt.rc('axes', titlesize=MEDIUM_FONT_SIZE)    # fontsize of the axes title
    # fontsize of the x and y labels
    plt.rc('axes', labelsize=MEDIUM_FONT_SIZE)
    plt.rc('xtick', labelsize=SMALL_FONT_SIZE)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_FONT_SIZE)    # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_FONT_SIZE)    # legend fontsize
    # major tick size in points
    mpl.rcParams['xtick.major.size'] = TICKS_LENGTH
    mpl.rcParams['xtick.minor.size'] = TICKS_LENGTH / \
        1.5  # minor tick size in points
    # major tick width in points
    mpl.rcParams['xtick.major.width'] = TICKS_LINEWIDTH
    # minor tick width in points
    mpl.rcParams['xtick.minor.width'] = TICKS_LINEWIDTH
    # major tick size in points
    mpl.rcParams['ytick.major.size'] = TICKS_LENGTH
    mpl.rcParams['ytick.minor.size'] = TICKS_LENGTH / \
        1.5  # minor tick size in points
    # major tick width in points
    mpl.rcParams['ytick.major.width'] = TICKS_LINEWIDTH
    # minor tick width in points
    mpl.rcParams['ytick.minor.width'] = TICKS_LINEWIDTH
    mpl.rcParams['text.color'] = DEFAULT_COLOR
    mpl.rcParams['axes.labelcolor'] = DEFAULT_COLOR
    mpl.rcParams['xtick.color'] = DEFAULT_COLOR
    mpl.rcParams['ytick.color'] = DEFAULT_COLOR
    mpl.rcParams['lines.linewidth'] = CURVE_LINEWIDTH
    mpl.rcParams['axes.linewidth'] = AXES_LINEWIDTH

    plt.rcParams['axes.grid'] = GRID


except Exception as e:
    print('Error loading Plotting configuration.')


def plot_figure(rows, cols):
    return plt.subplots(rows, cols, figsize=(FIGWIDTH, FIGHEIGHT * rows))


def custom_plot(x, y, ax=None, **plt_kwargs):
    if ax is None:
        ax = plt.gca()
    try:
        config = plt_kwargs['plot_config']

        x_key = closest_string(config.keys(), x.name)
        if x_key:
            x_tick_interval = config[x_key]['major_ticks']
            x_ticks = config[x_key]['minor_ticks']
            x_min = config[x_key]['min']
            x_max = config[x_key]['max']
        else:
            x_min = x_max = None
            x_tick_interval = x_ticks = -1

        y_key = closest_string(config.keys(), y.name)
        if y_key:
            y_tick_interval = config[y_key]['major_ticks']
            y_ticks = config[y_key]['minor_ticks']
            y_min = config[y_key]['min']
            y_max = config[y_key]['max']
            marker = config[y_key]['marker']
            curve_type = config[y_key]['curve_type']
        else:
            marker = y_min = y_max = None
            y_tick_interval = y_ticks = -1
            curve_type = 0

    except:
        marker = x_min = x_max = y_min = y_max = None
        x_tick_interval = y_tick_interval = x_ticks = y_ticks = -1
        curve_type = 0

    if 'plot_config' in plt_kwargs.keys():
        del plt_kwargs['plot_config']
    if type(marker) == int:
        marker = MARKERS[marker]
    if curve_type == 0:
        ax.plot(x, y, marker=marker, **plt_kwargs)
    else:
        X, Y, *_ = fit_data(x, y, curve_type)
        ax.plot(X, Y, **plt_kwargs)
        ax.scatter(x, y, marker=marker, ** plt_kwargs)

    if x_tick_interval != -1:
        ax.xaxis.set_major_locator(ticker.MultipleLocator(x_tick_interval))
    if y_tick_interval != -1:
        ax.yaxis.set_major_locator(ticker.MultipleLocator(y_tick_interval))
    x_ticks = None if x_ticks == -1 else x_ticks
    y_ticks = None if y_ticks == -1 else y_ticks
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(x_ticks))
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(y_ticks))
    if x_min != None:
        ax.set_xlim(left=x_min)

    if x_max != None:
        ax.set_xlim(right=x_max)

    if y_min != None:
        ax.set_ylim(bottom=y_min)

    if y_max != None:
        ax.set_ylim(top=y_max)

    return ax


def display_save_fig(fig, image_file_path):
    plt.tight_layout()
    plt.show()
    fig.savefig(image_file_path, bbox_inches='tight')
    print('Graph saved to file: '+image_file_path)


def modify_axis(axis, index, ylabel, color):

    if index == 0:
        axis.set_ylabel(ylabel, color=color)
        axis.spines['left'].set_color(color)
        axis.tick_params(axis='y', which='both', colors=color)
    else:
        axis.set_ylabel(ylabel, color=color)
        axis.spines['right'].set_position(('outward', 80*(index-1)))
        axis.spines['right'].set_color(color)
        axis.tick_params(axis='y', which='both', colors=color)
        axis.grid(False)


def composite_plot_with_axes(X, Y, y_axis_indices=[], xlabel=None, title=None, **plt_kwargs):
    if not y_axis_indices:
        y_axis_indices = list(range(len(Y)))
    if len(Y) > len(y_axis_indices):
        raise ValueError('Not enough values specifying Y-axes')
    if len(Y) < len(y_axis_indices):
        raise ValueError('Too many values specifying Y-axes')
    fig, ax = plot_figure(1, 1)

    axes = [ax]
    for _ in range(max(y_axis_indices)):
        axes.append(ax.twinx())
    axes[0].set(xlabel=xlabel, title=title)
    shared_axes = set(
        [x for x in y_axis_indices if y_axis_indices.count(x) > 1])
    for index in range(len(Y)):
        y = Y[index]
        axis_index = y_axis_indices[index]
        color = 'black' if axis_index in shared_axes else COLORS[index]
        y_label = 'Shared axis' if axis_index in shared_axes else y.name
        modify_axis(axes[axis_index], axis_index, y_label, color)

        custom_plot(X, y, color=COLORS[index],
                    ax=axes[axis_index], **plt_kwargs)

    return fig


def composite_plot(X, Y, xlabel=None, title=None, **plt_kwargs):

    fig, ax = plot_figure(1, 1)
    for index, y in enumerate(Y):

        if index == 0:
            ax.set(xlabel=xlabel, title=title)
            custom_plot(X, y, color=COLORS[index], **plt_kwargs)
            ax.set_ylabel(y.name, color=COLORS[index])
            ax.spines['left'].set_color(COLORS[index])
            ax.tick_params(axis='y', which='both', colors=COLORS[index])
        else:
            sensor = ax.twinx()
            custom_plot(X, y, color=COLORS[index], ax=sensor, **plt_kwargs)
            sensor.set_ylabel(y.name, color=COLORS[index])
            sensor.spines['right'].set_position(('outward', 80*(index-1)))
            sensor.spines['right'].set_color(COLORS[index])
            sensor.tick_params(axis='y', which='both', colors=COLORS[index])
            sensor.grid(False)
    return fig
