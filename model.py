from sentence_transformers import SentenceTransformer, models, InputExample, losses, util
from torch.utils.data import DataLoader
import torch
import pandas as pd
import compute_statistics as cs
import graph_generator as gg

##### - Model - #####

## Layer 1 - BERT Layer
# define our word-embedding layer => sentence-transformers/all-MiniLM-L6-v2
# Not truncating the sequencing length
word_embedding_model = models.Transformer("sentence-transformers/all-MiniLM-L6-v2")

## Layer 2 - Mean Pooling Layer
pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())

model = SentenceTransformer(modules=[word_embedding_model, pooling_model])

###### - Fine tuning  - ######

QUESTIONS_DATA_PATH='data/train_questions.csv' 
DOCUMENTS_DATA_PATH='data/train_documents.csv' 

## Reading CSV data files as dataframes
df_questions = pd.read_csv(QUESTIONS_DATA_PATH)
df_documents = pd.read_csv(DOCUMENTS_DATA_PATH) 

## building train_example pairs format : [query,document]
train_examples = []
for i in range(len(df_questions)):
    for j in range(len(df_documents)):
        if (df_questions.iloc[i,0] == df_documents.iloc[j,0]):
            train_examples.append(InputExample(texts = [df_questions.iloc[i,1], df_documents.iloc[j,1]], label=1.0))

def train():

    ## Train loader        
    train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)
    
    epochs = 10
    warmup_steps = int(len(train_dataloader) * epochs * 0.1)

    ## Loss function
    train_loss = losses.CosineSimilarityLoss(model)

    ## Fine tune Tune the model
    train = model.fit(
        train_objectives=[(train_dataloader, train_loss)], 
        epochs=epochs, 
        warmup_steps=warmup_steps,
        optimizer_class=torch.optim.AdamW,
        optimizer_params={'lr': 2e-5},
        output_path='output',
        save_best_model=True
    )

## if have gpu or cpu 
use_cuda = torch.cuda.is_available()
if use_cuda:
    print("device: cuda: ", 2)
    torch.cuda.set_device(2)
    torch.cuda.manual_seed(72)

## Fine Tuning the model ##
train()


###### - Testing  - ######


TEST_QUESTIONS_DATA_PATH='data/test_questions.csv' 
TEST_DOCUMENTS_DATA_PATH='data/test_documents.csv' 

df_test_questions = pd.read_csv(TEST_QUESTIONS_DATA_PATH)
df_test_documents = pd.read_csv(TEST_DOCUMENTS_DATA_PATH)

actual_list=[]
predicted_list=[]
reciprocal_ranks_list = []

bug_dic = {0:"200"} ## 1. Add issue list here
for bug_report_id in range(len(bug_dic)):
    
    ## Bug report embedding
    bug_report_id=0
    bug_report = df_test_questions.iloc[bug_report_id,1] #1st query
    bug_report_embedding = model.encode(bug_report)
    test_examples = []
    dic = {}
    
    # Documents relevant to above Bug report
    for j in range(len(df_test_documents)):
        if (df_test_questions.iloc[bug_report_id,0] == df_test_documents.iloc[j,0]):
            test_examples.append(df_test_documents.iloc[j,1])
            dic[df_test_documents.iloc[j,1]] = df_test_documents.iloc[j,2] # {document : url}

    # Encode all sentences
    embeddings = model.encode(test_examples)
    all_sentence_combinations = []

    # Compute cosine similarity between bug report and relevant documents
    cos_sim_values = []
    for document_id in range(len(embeddings)):
        cos_sim = util.cos_sim(bug_report_embedding, embeddings[document_id])
        all_sentence_combinations.append([cos_sim, bug_report_id, document_id])
        
    # #Sort list by the highest cosine similarity score
    all_sentence_combinations = sorted(all_sentence_combinations, key=lambda x: x[0], reverse=True)

    # get  most similar pairs:
    search_results = []
    rank = 1
    for score, i, j in all_sentence_combinations:
        result_row = {}
        result_row['bug_id'] = bug_dic[i]
        result_row['url'] = dic[test_examples[j]]
        result_row['cos_sim_score'] = "{:.4f}".format(score.item())
        result_row['rank'] = rank
        search_results.append(result_row)
        rank = rank + 1
    
    # Top-100 search results
    search_results = search_results[:100]   
    
    search_results = pd.DataFrame(search_results)
    search_results['bug_id']=search_results['bug_id'].astype(int)

    ## Actual Ranked list
    df1 = df_test_documents[['bug_id', 'url', 'relevancy_score']][:100]

    ## Predicted ranked list
    labeled_search_results = search_results.merge(df1, how='left', on=['bug_id', 'url']).fillna(0)
    labeled_search_results.to_csv('results/predicted_results.csv')
    
    ## Predicted Source File List
    relevances_rank = labeled_search_results.groupby(['bug_id', 'relevancy_score'])['rank'].min()

    ## consider only the relevancy score = 1 items
    ranks = relevances_rank.loc[:, 1]
    
    ## compute MRR
    reciprocal_ranks = 1 / (ranks)

    reciprocal_ranks_list.append(reciprocal_ranks)

    actual_list.append([float(i) for i in list(df1['relevancy_score'])])
    predicted_list.append(list(labeled_search_results['relevancy_score']))

## Compute MRR
# print("MRR@100", reciprocal_ranks_list[0].mean())
# MRR@100 0.03571428571428571

## Compute MAP
yMAPList = []
xMAPList = []
for i in range(20, 100, 10):
    map = cs.mapk(actual_list[:i],predicted_list[:i],k=i)
    yMAPList.append(map)
    xMAPList.append(i)

###### - Generate Graphs - ######    
## MAP graph ### 
gg.generate_map_graph(xMAPList, yMAPList)