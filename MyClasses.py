import csv

def kt_rong(data) :
    if data =="" :
        return "N/A"
    else:
        return data
def save_to_csv(data,filename,title):
    file_name = f"data/{filename}.csv"
    with open(file_name, mode='w', newline='',encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(title)
        for dat in data :
            writer.writerow(dat)
    print("DONE")
