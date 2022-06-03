import configparser
import os

import pandas as pd


def closest_string(strings, string):
    for s in strings:
        if s in string:
            return s
    print('not found')


def new_file_name(original_name, suffix, ext):
    new_name = original_name.split('.')
    new_name[-2] += suffix
    new_name[-1] = ext
    return ''.join(new_name)


def get_df(filepath, sep):
    return pd.read_csv(filepath, sep=sep)


def load_plot_config(config_path):
    try:
        config_path = os.path.join(config_path, 'config.ini')
        plot_config = {}
        config = configparser.ConfigParser()
        config.read(config_path)
        try:
            plot_config = eval(config['DEFAULT']['PLOT'])

        except Exception as e:
            print('Plot configuration not found: ', e)

    except Exception as e:
        print('Error loading configuration file: ', e)
    return plot_config


def create_plot_config(columns, path):

    try:
        config = configparser.ConfigParser()  # Initialise Configuration

        config['DEFAULT'] = {'plot': {column: {'min': None, 'max': None, 'major_ticks': -1, 'minor_ticks': -1, 'marker': None, 'curve_type': 0}
                                      for column in columns}}
        config_file = os.path.join(path, 'config.ini')
        with open(config_file, 'w') as configfile:
            config.write(configfile)

        print('Config saved in '+config_file)
    except:
        print('Could not save config.')


def create_folder(basepath, new_folder_name):
    if not os.path.exists(os.path.join(basepath, new_folder_name)):
        os.mkdir(os.path.join(basepath, new_folder_name))
    return os.path.join(basepath, new_folder_name)


def sequenced_file_name(basepath, name, ext):
    counter = 0
    filename = "{}{}.{}"
    while os.path.isfile(os.path.join(basepath, filename.format(name, counter, ext))):
        counter += 1
    return os.path.join(basepath, filename.format(name, counter, ext))


def create_folder_for_file(filepath):
    basepath, filename = os.path.split(filepath)
    new_folder_name = os.path.splitext(filename)[0]
    return create_folder(basepath, new_folder_name)


def config_exists(path):
    return os.path.isfile(os.path.join(path, 'config.ini'))
