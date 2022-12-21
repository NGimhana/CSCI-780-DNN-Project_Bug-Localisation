import os
import utils
import json
import pandas as pd

root_location = utils.root_location
results = []

field_names = ['bug_id', 'document', 'url']

test_file = "../data/test_documents.csv"

bug_ids = ["200"]
results = []
for bug_id in range(len(bug_ids)):

    directory = root_location + "/data/Buggy_projects/bug-" + bug_ids[bug_id]

    

    ## Get the Java Source files only
    def iterate_files(directory):
        for filename in os.scandir(directory):
            if filename.is_file():
                if filename.name.endswith(".java"):
                    document = {}
                    with open(filename, 'r', newline='', encoding='UTF-8',errors='ignore') as f:
                        document_content = ""
                        for line in f:
                            document_content = document_content + line.strip()     
                    document['bug_id'] = bug_ids[bug_id]  
                    document['document'] = document_content
                    document['url'] = filename.name
                    results.append(document) 
            else :
                iterate_files(filename)

    ## Navigate in BugLocation JSON files dir - Check JSON validation first!!
    dir_list = os.listdir(root_location + '/data/bug_fix_json/')

    iterate_files(directory)
    # # Write Results to CSV
    utils.list_to_csv_write_by_lines(test_file, field_names, results)  

    ## check the relevancy grade
    relevant_files = []

    with open(root_location + '/data/bug_fix_json/' + bug_ids[bug_id] + ".json") as json_file:
        json_data = json.load(json_file)
                        
        for fix_location in json_data['fix_location']:
            relevant_files.append(fix_location['file_name'])


    field_names = ['bug_id', 'document', 'url', 'relevancy_score']
    results = []
    df = pd.read_csv(test_file)

    for i in range(len(df)):
        results_row = {}
        results_row['bug_id'] = df.iloc[i,0]
        results_row['document'] = df.iloc[i,1]
        results_row['url'] = df.iloc[i,2]
        results_row['relevancy_score'] = 0
        for file in relevant_files:
            if file.__contains__(df.iloc[i,2]):
                results_row['relevancy_score'] = 1
                break
        results.append(results_row)    

# # Write Results to CSV
utils.list_to_csv_write_by_lines(test_file, field_names, results)              
    


          
