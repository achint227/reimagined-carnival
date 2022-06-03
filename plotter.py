import argparse

from basic_functions import (config_exists, create_folder,
                             create_folder_for_file, create_plot_config,
                             get_df, load_plot_config, sequenced_file_name)
from plot2d import composite_plot, composite_plot_with_axes, display_save_fig


def plot_my_2d_graph(filepath, x_index=0, createconfig=False, sep=';', exclude='', y_axis_indices=''):
    '''
    Creates a plot from the specified parameters saved into a PNG file
    The image is stored in a folder based on the dimensionality of the plot,
    that is contained inside a new folder named and created in the same directory as the input file. 

        Parameters:
            filepath: Path of the file to be used as data for plotting
            x_index: Index of the datastream to be used as X-axis in the plot, default zeroth index
            y_indices: Indices of axes for corresponding data streams, defalt empty string.
            createconfig: whether to create new plot configuration for the data, default False
            sep: Delimiter used in the csv file, default semicolon
            exclude: List of indices to be excluded, default empty string. '2,3'
            y_axis_indices: List of indices of axes for respective datastreams. '0,1'  
    '''

    graph_df = get_df(filepath, sep)
    x_axis = graph_df.columns[x_index]
    basepath = create_folder_for_file(filepath)

    basepath = create_folder(basepath, 'Two_dimensional_plots')
    excluded = [x_axis]
    if exclude:
        excluded_indices = [int(x) for x in exclude.split(',')]
        excluded.extend([graph_df.columns[i] for i in excluded_indices])
    y_axis_indices = [int(x) for x in y_axis_indices.split(',')]
    columns = [sensor for sensor in graph_df.columns]
    X = graph_df[x_axis]
    Y = [graph_df[sensor] for sensor in columns if sensor not in excluded]

    if not config_exists(basepath) or createconfig:
        create_plot_config(columns, basepath)
    plot_config = load_plot_config(basepath)
    result_file_path = sequenced_file_name(basepath, 'plot', 'png')
    fig = composite_plot_with_axes(
        X, Y, y_axis_indices, xlabel=X.name, plot_config=plot_config)
    display_save_fig(fig, result_file_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", type=str,
                        help="Filepath for input data")
    parser.add_argument("x_axis", type=int,
                        help="Index of sensor to be used as x-axis")
    parser.add_argument("y_indices", type=str,
                        help="Axis indices of corresponding data:  0,1,2,3,3", default="")
    parser.add_argument("-c", "--createconfig", help="create config file before plotting",
                        action="store_true")
    parser.add_argument("-s", "--sep", type=str, help="delimiter used in the csv file.",
                        default=";")
    parser.add_argument("-x", "--exclude", type=str, help="list of indices to exclude: 1,2,3",
                        default="")

    args = parser.parse_args()

    plot_my_2d_graph(args.filepath, args.x_axis,
                     args.createconfig, args.sep, args.exclude, args.y_indices)
