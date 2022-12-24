# CSCI-780-DNN-Project

## Collected Android GUI Bug-Solution DataSet

Buildup the evaluation data - AntroR2, with additional (37) bugs and corresponding ground truth data for bug localization
* Collected Bug-Solution pairs => https://drive.google.com/drive/u/0/folders/1Y8FL42F6YleZDKoDsgkiibygPmodjFdK

* Collected Buggy Source Codes => https://drive.google.com/drive/u/0/folders/1EPsFpq6P5S1N4UW0UbOeg8e7WHz-hVxp

* Collected Fixed Source Codes => https://drive.google.com/drive/u/0/folders/18XOgFirP4bHLiCjjM9Mgl57UKnmQhSUt

## Run

1. Download ```issues.json``` and ```Dataset_ AndroR2.csv``` from https://drive.google.com/drive/folders/1BKnVBdeN4sok04gXe_n-kWyrwaU0Ck01?usp=sharing. And extract those to ```data/raw_data``` directory.

2. Download the corpus(projects) from https://drive.google.com/drive/folders/1UMSss7LbpZVgx00v3MttArkvcDuepAK_?usp=sharing 

3. Unzip the projects in to data/Buggy_projects directory. 
The folder hierachy should be like below. Remove temp files/zips.
   ```
    ├── data                    
        ├── Buggy_projects          
            ├── bug-18
            ├── bug-1096
            ├── bug-2 
            ├── bug-10 
            ├── bug-1147 
            ├── bug-209 
            ├── bug-8 
            ├── bug-53
            ├── bug-128
            ├── bug-200         
            └── bug-1073
    ```
4. Download the bug_fix_json from https://drive.google.com/drive/folders/1zzBNebhY9LFv72fCu1U0D_R1GOzlIJNN?usp=sharing. And extract those to data/bug_fix_json directory.

```
    ├── data                    
        ├── bug_fix_json          
            ├── 18.json
            ├── 1096.json
            ├── 2.json 
            ├── 10.json 
            ├── 1147.json 
            ├── 209.json 
            ├── 8.json 
            ├── 53.json
            ├── 128.json
            ├── 200.json         
            └── 1073.json
```

5. Execute below command to create Conda virtual environment

```
conda env create -f environment.yml
conda activate bug_localisation
```

6. Copy the Absolute path of the project, and paste it in the ```data_generation_scripts/utils.py``` line 7 This is the root_location of the parent project.

7. Navigate to ```data_generation_scripts``` directory and execute ```python 1_bug_report_generator.py```


8. Now execute the ```python 2_query_generator.py``` to generate the queries - (bug reports)

9. Now execute the ```python 3_document_generator.py``` to generate the documents - (answers to the queries i.e files that had the actual bug in the source code)

10. Now execute the ```python 4_test_generator.py``` to generate the documents - (answers to the queries i.e files that had the actual bug in the source code)

11. Execute ```python model.py``` to finetune the model and generate results.
