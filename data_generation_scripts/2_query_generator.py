import os
import utils

results = []

directory = '../data/BR-Raw'
field_names = ['bug_id', 'query']
file = "../data/train_questions.csv"

bug_file = open('../data/raw_data/projectList.txt', 'r')
bug_list = bug_file.read().splitlines()

def iterate_files(directory):
    for filename in os.scandir(directory):
        if filename.is_file() :
            if filename.name.endswith(".txt") and (filename.name.split(".")[0]) in bug_list:
                bug_report = {}
                with open(filename, 'r', newline='', encoding='UTF-8',errors='ignore') as f:
                    query = ""
                    for line in f:
                        query = query + line.strip()
                bug_report['bug_id'] = os.path.basename(filename.name.split(".")[0])   
                bug_report['query'] = query
                results.append(bug_report) 
        else :
            iterate_files(filename)




iterate_files(directory)

# Write Results to CSV
utils.list_to_csv_write_by_lines(file, field_names, results)


############################################ 
###### TEST Questions generator
bug_file = open('../data/raw_data/test_projectList.txt', 'r')
bug_list = bug_file.read().splitlines()
results = []

test_file = "../data/test_questions.csv"

def iterate_files(directory):
    for filename in os.scandir(directory):
        if filename.is_file() :
            if filename.name.endswith(".txt") and (filename.name.split(".")[0]) in bug_list:
                bug_report = {}
                with open(filename, 'r', newline='', encoding='UTF-8',errors='ignore') as f:
                    query = ""
                    for line in f:
                        query = query + line.strip()
                bug_report['bug_id'] = os.path.basename(filename.name.split(".")[0])   
                bug_report['query'] = query
                results.append(bug_report) 
        else :
            iterate_files(filename)




iterate_files(directory)

# Write Results to CSV
utils.list_to_csv_write_by_lines(test_file, field_names, results)


