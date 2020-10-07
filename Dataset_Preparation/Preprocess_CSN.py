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

# %% [markdown]
# # Output Location

# %%
divs = ["test", "valid", "train"]
OUTPUT_FOLDER = "data/csn_preprocessed_data/java/final/jsonl/"
for div in divs:
    folder = OUTPUT_FOLDER+div+"/"
    os.system('mkdir -p $folder')


# %%
AVOID_DICT = {}
SEPARATOR = '<SEP>'
NUM_EXAMPLE_PER_FILE = 30000

# %% [markdown]
# # Tokenize and Create test and valid sets

# %%
from Tokenizer.CodePreprocess_final import code_filter
from Tokenizer.NLPreprocess_final import nl_filter


# %%
CSN_code_filter_flags = {
    "tokenize and remove_comments": "true",
    "remove_escape_charaters": "true",
    "subtokenize_camel_case": "true",   
    "subtokenize_snake_case": "true", 
    "subtokenize_str_int_str": "true", 
    "replace_string_literal_with": "none", 
    "replace_int_literal_with": "none", 
    "replace_float_literal_with": "none",  
    "replace_bool_literal_with": "none", 
    "remove_non_ascii": "true", 
    "delete_when_total_token_is_less_than": 3, 
    "maximum_length": 100000
}

with open('code_filter_flag.json', 'w') as outfile:
    json.dump(CSN_code_filter_flags, outfile, indent=2)
    outfile.close()

CSN_nl_filter_flags = {
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
    json.dump(CSN_nl_filter_flags, outfile, indent=2)
    outfile.close()


# %%
INPUT_FOLDER = "data/original_data/CSN/"
divs = ["test", "valid"]
err = 0
empty = 0

for div in divs:
    in_file_name = "java_{}_0.jsonl".format(div)
    print(in_file_name)

    
    input_file = open(INPUT_FOLDER+div+"/"+in_file_name, 'r')
    input_lines = input_file.readlines()
    input_file.close()
    in_data = [json.loads(jline) for jline in input_lines]
    
    out_data = []
    
    for idx in range(len(in_data)):
        try:
            in_data[idx]['docstring'] = nl_filter(in_data[idx]['docstring'], CSN_nl_filter_flags).encode("utf-8", errors="ignore").decode().strip() 
            in_data[idx]['docstring_tokens'] = in_data[idx]['docstring'].split()
            
            in_data[idx]['code'] = code_filter(in_data[idx]['code'], CSN_code_filter_flags).encode("utf-8", errors="ignore").decode().strip() 
            in_data[idx]['code_tokens'] = in_data[idx]['code'].split()
            
            if in_data[idx]['docstring'].strip() == "" or in_data[idx]['code'].strip() == "":
                empty += 1
                continue
            
            out_data.append(in_data[idx])
            
            AVOID_DICT[in_data[idx]['code']+SEPARATOR+in_data[idx]['docstring']] = 1
            
        except:
            err += 1
            continue
        
    out_file_name = OUTPUT_FOLDER+div+"/"+"java_{}_0.jsonl".format(div)    
    out_file = open(out_file_name, 'w', encoding="utf-8")
    writer = jsonlines.Writer(out_file)
    writer.write_all(out_data)
    writer.close()
    out_file.close()

    os.system('gzip -f $out_file_name')
        
    print("Tokenization Error :", err)
    print("Empty NL or Code :", empty) 
    print("Remaining :", len(out_data))
    
    del in_data
    del out_data
    gc.collect()

    

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
# # Initial Selection of IDs for train set

# %%
source_ids = range(len(CoDesc_data))
test_ids = src2id_dict['CodeSearchNet-Java']["test"]
valid_ids = src2id_dict['CodeSearchNet-Java']["valid"]

truncated_ids = src2id_dict['CodeSearchNet-Py2Java']["truncated"]

print(len(valid_ids)) # 14141
print(len(test_ids)) # 25246
print(len(truncated_ids)) # 21616


# %%
avoid_ids = []
avoid_ids.extend(test_ids)
avoid_ids.extend(valid_ids)
avoid_ids.extend(truncated_ids)
print(len(avoid_ids)) # 61003

avoid_id_dict = {}
for a_id in avoid_ids:
    avoid_id_dict[a_id] = 1


# %%
train_ids_pass1 = []

for candidate_id in source_ids:
    if candidate_id % 1000000 == 0:
        print(datetime.datetime.now(), ":", candidate_id)
    try:
        string = avoid_id_dict[candidate_id]
    except KeyError:
        train_ids_pass1.append(candidate_id)
    
print(len(train_ids_pass1)) # 4150513

# %% [markdown]
# # Duplicate Removal

# %%
avoid_ids = []
avoid_ids.extend(test_ids)
avoid_ids.extend(valid_ids)

for a_id in avoid_ids:
    avoid_str = CoDesc_data[a_id]['code']+SEPARATOR+CoDesc_data[a_id]['nl']
    AVOID_DICT[avoid_str] = 1


# %%
train_ids_pass2 = []
empty = 0

for candidate_id in train_ids_pass1:
    if candidate_id % 1000000 == 0:
        print(datetime.datetime.now(), ":", candidate_id)
    
    if CoDesc_data[candidate_id]['code'].strip() == "" or CoDesc_data[candidate_id]['nl'].strip() == "":
        empty += 1
        continue
        
    check_str = CoDesc_data[candidate_id]['code']+SEPARATOR+CoDesc_data[candidate_id]['nl']
    
    try:
        mystr = AVOID_DICT[check_str]
    except KeyError:
        AVOID_DICT[check_str] = 1
        train_ids_pass2.append(candidate_id)
    


# %%
print("EMPTY NL or code :", empty) # 0
print("Duplicate :", (len(train_ids_pass1)-len(train_ids_pass2)-empty)) # 0
print("REMAINING TRAIN:", len(train_ids_pass2)) # 4150513


# %%
del AVOID_DICT
del avoid_ids
del avoid_id_dict
gc.collect()

# %% [markdown]
# # Creating train set

# %%
train_ids = train_ids_pass2
id_dict = {}
id_dict['train'] = train_ids


# %%
def create_sample(sample_id, tokenized_code, tokenized_nl, partition):
    sample = {}
    sample['id'] = sample_id
    sample['repo'] = "REPO"
    sample['path'] = "PATH"
    sample['func_name'] = "FUNC_NAME"
    
    try:
        sample['original_string'] = tokenized_code.encode("utf-8", errors="ignore").decode()  
    except:
        return None
    
    sample['language'] = "java"
    
    sample['code'] = sample['original_string']
    sample['code_tokens'] = sample['code'].split()  

    try:
        sample['docstring'] = tokenized_nl.encode("utf-8", errors="ignore").decode()    
    except:
        return None
    
    sample['docstring_tokens'] = sample['docstring'].split()
    
    sample['sha'] = "SHA"
    sample['url'] = "URL"
    sample['partition'] = partition
    
    return sample
 


# %%
div = "train"

train_data = []
file_idx = 0
for sample_id in train_ids:
    sample_dict = create_sample(sample_id, CoDesc_data[sample_id]['code'], CoDesc_data[sample_id]['nl'], div)

    if sample_dict is None:
        id_dict[div].remove(sample_id)
        continue

    train_data.append(sample_dict)
    
    if len(train_data) >= NUM_EXAMPLE_PER_FILE:
        print(file_idx)
        out_file_name = OUTPUT_FOLDER+div+"/"+"java_{}_{}.jsonl".format(div, file_idx)
        out_file = open(out_file_name, 'w', encoding="utf-8")
        writer = jsonlines.Writer(out_file)
        writer.write_all(train_data)
        writer.close()
        out_file.close()

        os.system('gzip -f $out_file_name')

        del train_data
        gc.collect()
        
        train_data = []
        file_idx += 1
        

out_file_name = OUTPUT_FOLDER+div+"/"+"java_{}_{}.jsonl".format(div, file_idx)
out_file = open(out_file_name, 'w', encoding="utf-8")
writer = jsonlines.Writer(out_file)
writer.write_all(train_data)
writer.close()
out_file.close()

os.system('gzip -f $out_file_name')

print("total =", file_idx*NUM_EXAMPLE_PER_FILE+len(train_data)) # 4150513

del train_data
gc.collect()


# %%
with open(OUTPUT_FOLDER.replace("java/final/jsonl/", "")+"csn_train_ids.json", 'w') as outfile:
    json.dump(id_dict, outfile)
    outfile.close()

# %% [markdown]
# # Clean Memory

# %%
del CoDesc_data
del src2id_dict
del id_dict

gc.collect()


