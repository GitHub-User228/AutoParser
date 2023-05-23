import csv

def save_as_txt(file, storage_path, filename):
    with open(f'{storage_path}/{filename}.txt', 'a') as f:
        for item in file:
            f.write(f'{item}\n')


def save_as_csv(file, storage_path, filename):
    with open(f'{storage_path}/{filename}.csv', 'a', encoding='utf8', newline='') as a,\
         open(f'{storage_path}/{filename}.csv', 'r') as r:
        lines = [row for row in csv.DictReader(r)]
        w = csv.writer(a)
        if len(lines) == 0:
            w.writerow(file.keys())
        w.writerows(zip(*file.values()))


def transfer_to_cluster(storage_path, filename):
    pass