import csv
import os


def kt_rong(data):
    if data == "":
        return "N/A"
    else:
        return data


def is_file_exists(file_path):
    return os.path.exists(file_path)

def save_to_csv(data, filename, title):
    file_name = f"data/{filename}.csv"
    if is_file_exists(file_name):
        title = ""
    with open(file_name, mode='a', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        if title != "":
            writer.writerow(title)
        for dat in data:
            writer.writerow(dat)
