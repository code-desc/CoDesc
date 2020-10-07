# %% [markdown]
# # Imports

# %%
import os
import shutil
import time
import datetime
import json
import jsonlines
import pickle
import sys
import gc
import numpy as np
import pandas as pd
import random 
import math


# %%
import multiprocessing
NUM_CORES = 6


# %%
ERROR_STRING = "__ERROR__"

# %% [markdown]
# # Output Location

# %%
OUTPUT_FOLDER = "data/ncs_preprocessed_data/"
    
divs = ["train-CoDesc", "train", "dev", "test"]
for div in divs:
    folder = OUTPUT_FOLDER+div+"/"
    os.system('mkdir -p $folder')


# %%
AVOID_DICT = {}
SEPARATOR = '<SEP>'

# %% [markdown]
# # Load CoDesc

# %%
CoDesc_FOLDER = "data/CoDesc/"


# %%
in_file = open(CoDesc_FOLDER+"CoDesc.json", 'r')
CoDesc_data = json.load(in_file)
in_file.close()


# %%
in_file = open(CoDesc_FOLDER+"src2id.json", 'r')
src2id_dict = json.load(in_file)
in_file.close()


# %%
# id2src_df = pd.read_csv(CoDesc_FOLDER+"id2src.csv")
# id2src_df


# %%
len(CoDesc_data) # 4211516


# %%
# Remove some fields to optimize memory consumption
for idx in range(len(CoDesc_data)):
    CoDesc_data[idx].pop('src')
    CoDesc_data[idx].pop('src_div')
    CoDesc_data[idx].pop('src_idx')
    CoDesc_data[idx].pop('original_code')
    CoDesc_data[idx].pop('original_nl')
gc.collect()

# %% [markdown]
# # Tokenizer

# %%
from Tokenizer.CodePreprocess_final import code_filter
from Tokenizer.NLPreprocess_final import nl_filter


# %%
NCS_code_filter_flags = {
    "tokenize and remove_comments": "true", 
    "remove_escape_charaters": "true",
    "subtokenize_camel_case": "true",  
    "subtokenize_snake_case": "true", 
    "subtokenize_str_int_str": "true", 
    "replace_string_literal_with": "STRING", # "as in original data"
    "replace_int_literal_with": "NUM", # "as in original data"
    "replace_float_literal_with": "NUM", # "as in original data"
    "replace_bool_literal_with": "BOOL", # "as in original data"
    "remove_non_ascii": "true", 
    "delete_when_total_token_is_less_than": 3, 
    "maximum_length": 100000
}

with open('code_filter_flag.json', 'w') as outfile:
    json.dump(NCS_code_filter_flags, outfile, indent=2)
    outfile.close()

NCS_nl_filter_flags = {
    "to_lower_case": "true",
    "tokenize": "true", 
    "remove_escape_charaters": "true", 
    "subtokenize_camel_case": "true", 
    "subtokenize_snake_case": "true", 
    "subtokenize_str_int_str": "true", 
    "remove_parameter_return_throws_info": "true", 
    "remove_non_ascii": "true", 
    "remove_comment_tags": "true",
    "remove_html_tags": "true", 
    "remove_@link_@code_@inheritDoc": "true", 
    "remove_begin_end_user_doc": "true",    
    "maximum_length": 50000, 
    "minimum_alphabet_count": 2, 
    "remove_unwanted_symbol": "true"  
}

with open('nl_filter_flag.json', 'w') as outfile:
    json.dump(NCS_nl_filter_flags, outfile, indent=2)
    outfile.close()

# %% [markdown]
# # Multiprocessing Tokenize CoDesc Codes and Save

# %%
# multiprocessing

def worker_function(worker_data, code_dict):
    print("WORKER START : ", worker_data[0]['id'], worker_data[-1]['id'])
    
    for sample in worker_data:
        if sample['id'] % 10000 == 0:
            print(datetime.datetime.now(), ":", sample['id'])
        
        try:
            code_dict[sample['id']] = code_filter(sample['code'], NCS_code_filter_flags).strip()
        except:
            code_dict[sample['id']] = ERROR_STRING
    
    print("WORKER END : ", worker_data[0]['id'], worker_data[-1]['id'])


# %%
manager = multiprocessing.Manager()
shared_code_dict = manager.dict()

worker_amount = math.floor(len(CoDesc_data)/NUM_CORES)

workers = []

for i in range(NUM_CORES):
    low = i*worker_amount
    if i == NUM_CORES-1:
        high = len(CoDesc_data)
    else:
        high = low+worker_amount
    
    w = multiprocessing.Process(target=worker_function, args=(CoDesc_data[low:high], shared_code_dict))
    workers.append(w)
    w.start()

for w in workers:
    w.join()
    


# %%
tokenized_code_dict = shared_code_dict.copy()

del shared_code_dict
gc.collect()


# %%
tokenized_code_dict[100]


# %%
CoDesc_data[100]


# %%
with open("data/ncs_tokenized_code.json", 'w') as outfile:
    json.dump(tokenized_code_dict, outfile, indent = 2)
    outfile.close()


# %%
del tokenized_code_dict
gc.collect()


# %%


# %% [markdown]
# # Tokenize and Create NCS test, valid, and train sets

# %%
AVOID_DICT = {}
SEPARATOR = '<SEP>'


# %%
divs = ["train", "dev", "test"]
INPUT_FOLDER = "data/original_data/"+"ncs/"

for div in divs:
    print(div)
    err = 0
    empty = 0
    success = 0
    
    code_file = open(INPUT_FOLDER+div+"/code.original_subtoken", 'r')
    code_lines = code_file.readlines()
    code_file.close()
    
    nl_file = open(INPUT_FOLDER+div+"/javadoc.original", 'r')
    nl_lines = nl_file.readlines()
    nl_file.close()
    
    code_file = open(OUTPUT_FOLDER+div+"/code.original_subtoken", 'w', encoding='ascii')
    nl_file = open(OUTPUT_FOLDER+div+"/javadoc.original", 'w', encoding='ascii')

    for idx in range(len(nl_lines)):
        try:
            tokenized_code = code_filter(code_lines[idx], NCS_code_filter_flags).encode('ascii', errors='ignore').decode().strip()
            tokenized_nl = nl_filter(nl_lines[idx], NCS_nl_filter_flags).encode('ascii', errors='ignore').decode().strip()
        except:
            err += 1
            continue
        
        if tokenized_code == "" or tokenized_nl == "":
            empty += 1
            continue
        
        AVOID_DICT[tokenized_code+SEPARATOR+tokenized_nl] = 1
        
        code_file.write(tokenized_code+"\n")
        nl_file.write(tokenized_nl+"\n")
        
        success += 1

    print("Error :", err)
    print("Empty :", empty)
    print("Success :", success)
    

    code_file.close()
    nl_file.close()
    
    del code_lines
    del nl_lines
    gc.collect()
    

# %% [markdown]
# # Load Tokenized Code 

# %%
in_file = open("data/ncs_tokenized_code.json", 'r')
tokenized_code_dict = json.load(in_file)
in_file.close()


# %%
for idx in range(len(CoDesc_data)):
    CoDesc_data[idx]['code'] = tokenized_code_dict[str(idx)].encode('ascii', errors='ignore').decode().strip()
    CoDesc_data[idx]['nl'] = CoDesc_data[idx]['nl'].encode('ascii', errors='ignore').decode().strip()


# %%
del tokenized_code_dict
gc.collect()


# %%
CoDesc_data[100]

# %% [markdown]
# # Initial Selection of IDs for train, valid and test sets

# %%
truncated_ids = src2id_dict['CodeSearchNet-Py2Java']["truncated"]
print(len(truncated_ids))


# %%
avoid_ids = []
avoid_ids.extend(truncated_ids)
print(len(avoid_ids))

avoid_id_dict = {}
for a_id in avoid_ids:
    avoid_id_dict[a_id] = 1


# %%
train_ids_pass1 = []

for candidate_id in range(len(CoDesc_data)):
    if candidate_id % 1000000 == 0:
        print(datetime.datetime.now(), ":", candidate_id)
    try:
        string = avoid_id_dict[candidate_id]
    except KeyError:
        train_ids_pass1.append(candidate_id)
    
print(len(train_ids_pass1))

# %% [markdown]
# # Duplicate Removal

# %%
train_ids_pass2 = []
errors = []
empty = []

for candidate_id in train_ids_pass1:
    if candidate_id % 1000000 == 0:
        print(datetime.datetime.now(), ":", candidate_id)
        
    check_str = CoDesc_data[candidate_id]['code']+SEPARATOR+CoDesc_data[candidate_id]['nl']
        
    if check_str.startswith(ERROR_STRING) or check_str.endswith(ERROR_STRING):
        errors.append(candidate_id)
        continue
    elif check_str.startswith(SEPARATOR) or check_str.endswith(SEPARATOR):
        empty.append(candidate_id)
        continue
    
    try:
        mystr = AVOID_DICT[check_str]
    except KeyError:
        AVOID_DICT[check_str] = 1
        train_ids_pass2.append(candidate_id)


# %%
print("ERROR PARSING CODE :", len(errors)) # 14163
print("EMPTY NL or Code :", len(empty)) # 0
print("Duplicate :", (len(train_ids_pass1)-len(train_ids_pass2)-len(empty)-len(errors))) # 83105
print("REMAINING TRAIN:", len(train_ids_pass2))


# %%
del AVOID_DICT
del avoid_ids
del avoid_id_dict
gc.collect()


# %%


# %% [markdown]
# # Creating train-CoDesc set

# %%
train_ids = train_ids_pass2
id_dict = {}
id_dict['train'] = train_ids


# %%
div = "train-CoDesc"
print(div)

code_file = open(OUTPUT_FOLDER+div+"/code.original_subtoken", 'w', encoding='ascii')
nl_file = open(OUTPUT_FOLDER+div+"/javadoc.original", 'w', encoding='ascii')


for sample_id in train_ids:
    code_file.write(CoDesc_data[sample_id]['code']+"\n")
    nl_file.write(CoDesc_data[sample_id]['nl']+"\n")

code_file.close()
nl_file.close()


# %%
with open(OUTPUT_FOLDER+"ncs-CoDesc_train_ids.json", 'w') as outfile:
    json.dump(id_dict, outfile)
    outfile.close()


# %%


# %% [markdown]
# # Clean Memory

# %%
del CoDesc_data
del src2id_dict
del id_dict
gc.collect()

