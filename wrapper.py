from plotter import plot_my_2d_graph


if __name__ == "__main__":

    filepath = 'test_file.csv'  # Path of the file to be used as data for plotting

    dimension = 2  # Dimensionality of the plot 2 or 3 for 2D or 3D respectively

    x_index = 0  # Index of the datastream to be used as X-axis in the plot

    createconfig = False  # Create new plot configuration for the data

    sep = ';'  # Delimiter used in the csv file

    exclude = '3'  # List of indices to be excluded. e.g. '2,3'

    y_axis_indices = '0,1,2'

    if dimension == 2:
        plot_my_2d_graph(filepath, x_index, createconfig,
                         sep, exclude, y_axis_indices)
