import numpy as np
import pandas as pd
import os


global avg_MAD


def get_ri(x_y_z_arr):
    """
    the accelerometer result in time i.
    :param x_y_z_arr: x, y, z values
    :return: (x^2 + y^2 + z^2)^-2
    """
    return pow((pow(x_y_z_arr[0], 2) + pow(x_y_z_arr[1], 2) + pow(x_y_z_arr[2], 2)), 0.5)


def avg_MAD():
    data_you_need = pd.DataFrame()
    for curr_accelerometer_file in os.listdir(r'C:\Users\mayah\PycharmProjects\CyberTraits\Data'):
        full_path_accelerometer_file = os.path.join(r'C:\Users\mayah\PycharmProjects\CyberTraits\Data',
                                                    curr_accelerometer_file)
        dirs = os.listdir(full_path_accelerometer_file + "\\accelerometer")
        for file in dirs:
            path = full_path_accelerometer_file + "\\accelerometer\\" + file
            accelerometer_df = pd.read_csv(path, usecols=['UTC time', 'x', 'y', 'z'])
            data_you_need = data_you_need.append(accelerometer_df, ignore_index=True)

    count_samples = int(data_you_need.shape[0])
    ri = pow((pow(data_you_need['x'], 2) + pow(data_you_need['y'], 2) + pow(data_you_need['z'], 2)), 0.5)
    ri_avg = sum(ri) / count_samples
    dis = (ri - ri_avg).abs()
    MAD = sum(dis) / count_samples
    print("Average MAD is: ", MAD)
    return MAD


avg_MAD=avg_MAD()


