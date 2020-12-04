# 将对应域名文件夹下的excel文件，提取源IP并转化UTC时间
import pandas
import os
import time


def utc_trans(sor_utc):
    the_sor_utc = int(sor_utc[:10])
    time_trans = time.localtime(the_sor_utc)
    time_str = time.strftime('%Y-%m-%d %H:%M:%S', time_trans)
    return time_str


def url_fix(the_folder_file_name):
    the_one_file_dataframe = pandas.DataFrame()
    the_one_file_data = pandas.read_csv(the_folder_file_name, header=None, sep='，')
    for the_one_row_str in the_one_file_data.iloc[:, 0]:
        the_one_row_info = the_one_row_str.split('|')
        time_start = utc_trans(the_one_row_info[0])
        time_end = utc_trans(the_one_row_info[1])
        sor_ip = the_one_row_info[2]
        the_one_fix_data = pandas.DataFrame(columns=['time_start', 'time_end', 'sor_ip'],
                                            data=[[time_start, time_end, sor_ip]])
        the_one_file_dataframe = the_one_file_dataframe.append(the_one_fix_data)
    return the_one_file_dataframe


if __name__ == '__main__':
    the_path = '\\hunantv.com'  # 修改位对应文件路径
    folder_file_path = os.getcwd() + the_path
    folder_file_names = os.listdir(folder_file_path)
    all_date = pandas.DataFrame()
    for folder_file_name in folder_file_names:
        if folder_file_name[-3:] == 'csv':
            one_fix_data = url_fix(folder_file_path + '\\' + folder_file_name)
            all_date = all_date.append(one_fix_data)
    all_date.to_excel(folder_file_path + '\\' + the_path[1:] + '.xlsx', header=None, index=None)
