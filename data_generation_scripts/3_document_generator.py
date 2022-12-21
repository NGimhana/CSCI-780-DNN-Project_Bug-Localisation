import os
import  json
import utils

root_location = utils.root_location
results = []

field_names = ['bug_id', 'document', 'url']
file = "../data/documents.csv"
train_file = "../data/train_documents.csv"

if not os.path.isdir("../data/Buggy_projects"):
    os.makedirs("../data/Buggy_projects")

if not os.path.isdir("../data/bug_fix_json"):
    os.makedirs("../data/Buggy_projects")    


## Issue List
issue_id_list_file = open(root_location + '/data/raw_data/projectList.txt')
issues = issue_id_list_file.readlines()

## Navigate in BugLocation JSON files dir - Check JSON validation first!!
dir_list = os.listdir(root_location + '/data/bug_fix_json/')


## Issues in the andror2-bugs.txt
# for issue_id in issues:
#     # Issues in the andror2 bug list
#     if int(issue_id) in brg.app_name_bug_id_dict.keys():
#         app_name = brg.app_name_bug_id_dict[int(issue_id)]
#         dir_path = root_location + "/" + "Goldset/" + app_name
#         if not os.path.exists(dir_path):
#             os.mkdir(dir_path)
          
def iterate_files(directory, file):
    filename = root_location + "/data/Buggy_projects/" + directory
    
    bug_report = {}
    with open(filename, 'r', newline='', encoding='UTF-8',errors='ignore') as f:
        document = ""
        for line in f:
            document = document + line.strip()
        bug_report['bug_id'] = os.path.basename(directory.split("/")[0].split("-")[1])   
        bug_report['document'] = document
        bug_report['url'] = file
        results.append(bug_report) 
    

for json_file in dir_list:
    if json_file.endswith(".json"):
        json_data = [] # your list with json objects (dicts)
        with open(root_location + '/data/bug_fix_json/' + json_file) as json_file:
            json_data = json.load(json_file)
        for issue_id in issues:
            if int(issue_id) == int(json_data['id']):
                for change_set in json_data['fix_location']:
                    ## Ignore First item in before the / => Eg; AppName/app .... here we ignore AppName
                    file_path = "bug-" + issue_id.strip() + "/" + "/".join(change_set['file_name'].split("/")[1:]).strip()
                    iterate_files(file_path, change_set['file_name'].strip())




# Write Results to CSV
utils.list_to_csv_write_by_lines(file, field_names, results) 
utils.duplicate_row_remover(file, train_file)                   

            


