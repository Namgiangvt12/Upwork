import os

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    folder_path = 'data/50.0015'
    # Lặp qua tất cả các tệp trong thư mục
    for filename in os.listdir(folder_path):
        if filename.startswith('50.0016_'):  # Kiểm tra tên tệp có bắt đầu bằng '50.0015_'
            new_filename = filename.replace('50.0016_', '50.0015_')  # Đổi tên tệp
            old_filepath = os.path.join(folder_path, filename)  # Đường dẫn đầy đủ của tệp cũ
            new_filepath = os.path.join(folder_path, new_filename)  # Đường dẫn đầy đủ của tệp mới
            os.rename(old_filepath, new_filepath)  # Đổi tên tệp

    print('Đổi tên các tệp thành công.')

