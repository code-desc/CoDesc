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
OUTPUT_FOLDER = "data/csn_preprocessed_data_balanced_partition/java/final/jsonl/"
for div in divs:
    folder = OUTPUT_FOLDER+div+"/"
    os.system('mkdir -p $folder')


# %%
NUM_EXAMPLE_PER_FILE = 30000

# %% [markdown]
# # Load CoDesc

# %%
CoDesc_FOLDER = "data/CoDesc/"


# %%
in_file = open(CoDesc_FOLDER+"CoDesc.json", 'r')
CoDesc_data = json.load(in_file)
in_file.close()


# %%
in_file = open(CoDesc_FOLDER+"partiton2id_dict.json", 'r')
partiton2id_dict = json.load(in_file)
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


# %%


# %% [markdown]
# # Creating train, valid and test set

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
divs = ["test", "valid", "train"]
for div in divs:
    div_data = []
    file_idx = 0
    for sample_id in partiton2id_dict[div]:
        sample_dict = create_sample(sample_id, CoDesc_data[sample_id]['code'], CoDesc_data[sample_id]['nl'], div)

        if sample_dict is None:
            id_dict[div].remove(sample_id)
            continue

        div_data.append(sample_dict)

        if len(div_data) >= NUM_EXAMPLE_PER_FILE:
            print(div, file_idx)
            out_file_name = OUTPUT_FOLDER+div+"/"+"java_{}_{}.jsonl".format(div, file_idx)
            out_file = open(out_file_name, 'w', encoding="utf-8")
            writer = jsonlines.Writer(out_file)
            writer.write_all(div_data)
            writer.close()
            out_file.close()

            os.system('gzip -f $out_file_name')

            del div_data
            gc.collect()

            div_data = []
            file_idx += 1


    out_file_name = OUTPUT_FOLDER+div+"/"+"java_{}_{}.jsonl".format(div, file_idx)
    out_file = open(out_file_name, 'w', encoding="utf-8")
    writer = jsonlines.Writer(out_file)
    writer.write_all(div_data)
    writer.close()
    out_file.close()

    os.system('gzip -f $out_file_name')

    print("total =", file_idx*NUM_EXAMPLE_PER_FILE+len(div_data)) # 4150513

    del div_data
    gc.collect()

# %% [markdown]
# # Clean Memory

# %%
del CoDesc_data
del partiton2id_dict

gc.collect()


