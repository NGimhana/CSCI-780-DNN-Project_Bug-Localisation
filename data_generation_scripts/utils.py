import csv
import os

root_location="/Users/bimalkadesilva/Desktop/CSCI-780-DNN-Project"

def list_to_csv_write_by_line(file_name, field_names, num_of_lines, results):
    with open(file_name, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        for i in range(num_of_lines):
            writer.writerow(results[i])


def list_to_csv_write_by_lines(file_name, field_names, results):
    with open(file_name, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(results)

def duplicate_row_remover(in_file_path,out_file_path):
    with open(in_file_path, 'r') as in_file, open(out_file_path, 'w') as out_file:
        seen = set() # set for fast O(1) amortized lookup
        for line in in_file:
            if line in seen: continue # skip duplicate
            seen.add(line)
            out_file.write(line)   
    if os.path.exists(in_file.name):
        os.remove(in_file.name)
    else:
        print("The file does not exist")
