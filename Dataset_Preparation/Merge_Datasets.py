# %%
import os
import sys
import pickle
import gc
import datetime
import random
import json
import jsonlines
import numpy as np
import pandas as pd


# %%
from Tokenizer.CodePreprocess_final import code_filter
from Tokenizer.NLPreprocess_final import nl_filter


# %%
code_filter_flags = {
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
    json.dump(code_filter_flags, outfile, indent=2)
    outfile.close()
 
nl_filter_flags = {
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
    json.dump(nl_filter_flags, outfile, indent=2)
    outfile.close()


# %%
DATA_FOLDER = "data/original_data/"
SEPARATOR = '<SEP>'

# %% [markdown]
# # CodeSearchNet-Java

# %%
INPUT_FOLDER = DATA_FOLDER+"CSN/"
divs = ["test/", "valid/", "train/"]


# %%
CSN_data = []
CSN_urls = {}

CSN_empty = 0

CSN_Avoid = {}
CSN_Dup = 0


# %%
for div in divs:
    src_idx = 0
    
    nums = range(1)
    if div == "train/":
        nums = range(16)
    
    for num in nums:
        in_file_name = "java_{}_{}.jsonl".format(div.replace("/", ""), num)
        print(datetime.datetime.now(), ":", in_file_name)
        
        input_file = open(INPUT_FOLDER+div+in_file_name, 'r')
        input_lines = input_file.readlines()
        input_file.close()
        in_data = [json.loads(jline) for jline in input_lines]
        
        for sample in in_data:        
            out_dict = {}
            
            out_dict['src'] = 'CodeSearchNet-Java'
            out_dict['src_div'] = div.replace("/", "")
            out_dict['src_idx'] = src_idx
            src_idx += 1
            
            out_dict['original_code'] = sample['code'].strip()
            out_dict['original_nl'] = sample['docstring'].strip()

            out_dict['code'] = code_filter(out_dict['original_code'], code_filter_flags).strip()
            out_dict['nl'] = nl_filter(out_dict['original_nl'], nl_filter_flags).strip()

            check_str = out_dict['code']+SEPARATOR+out_dict['nl']

            try:
                mystr = CSN_Avoid[check_str]
                CSN_Dup += 1
                continue
            except KeyError:
                if out_dict['nl'] == "" or out_dict['code'] == "":
                    CSN_empty += 1
                else:
                    CSN_data.append(out_dict)
                    CSN_urls[sample['url']] = 1
                CSN_Avoid[check_str] = 1
        
        del in_data
        del input_lines
        gc.collect()
        


# %%
print(len(CSN_data)) # 466971
print(CSN_Dup) # 14
print(CSN_empty) # 29703


# %%
print(CSN_data[0].keys())
print(CSN_data[-1])


# %%
# include the data points from whole corpus which were removed


# %%
corpus_file = open(INPUT_FOLDER+"java_dedupe_definitions_v2.pkl", 'rb')
corpus_data = pickle.load(corpus_file)
corpus_file.close()


# %%
print(len(corpus_data)) # 1569889
print(corpus_data[0].keys())
print(corpus_data[0])


# %%
removed_data = []

for idx in range(len(corpus_data)):
    if idx % 100000 == 0:
        print(datetime.datetime.now(), ":", idx)
    
    sample = corpus_data[idx]
    if sample['docstring'].strip() == "":
        continue
        
    try:
        my_str = CSN_urls[sample['url']]
        continue
    except KeyError:
        out_dict = {}

        out_dict['src'] = 'CodeSearchNet-Java'
        out_dict['src_div'] = "removed"
        out_dict['src_idx'] = idx

        out_dict['original_code'] = sample['function'].strip()
        out_dict['original_nl'] = sample['docstring'].strip()

        out_dict['code'] = code_filter(out_dict['original_code'], code_filter_flags).strip()
        out_dict['nl'] = nl_filter(out_dict['original_nl'], nl_filter_flags).strip()

        check_str = out_dict['code']+SEPARATOR+out_dict['nl']

        try:
            mystr = CSN_Avoid[check_str]
            CSN_Dup += 1
            continue
        except KeyError:
            if out_dict['nl'] == "" or out_dict['code'] == "":
                CSN_empty += 1
            else:
                removed_data.append(out_dict)
                CSN_urls[sample['url']] = 1
            CSN_Avoid[check_str] = 1
        
             

# %%
print(len(removed_data)) # 23198


# %%
print(removed_data[0].keys())
print(removed_data[0])


# %%
CSN_data.extend(removed_data)
print(len(CSN_data)) # 490169


# %%
print("TOTAL =", len(CSN_data)+CSN_Dup+CSN_empty) # 572708
print("Duplicate =", CSN_Dup) # 29731
print("Empty =", CSN_empty) # 52808


# %%
with open(DATA_FOLDER+"CSN_Data.json", 'w') as outfile:
    json.dump(CSN_data, outfile)
    outfile.close()
    


# %%
del corpus_data
del CSN_data
del removed_data
gc.collect()


# %%
CSN_file = open(DATA_FOLDER+"CSN_Data.json", 'r')
CSN_data = json.load(CSN_file)
CSN_file.close()


# %%
print(len(CSN_data)) # 490169


# %%
print(CSN_data[0].keys())
print(CSN_data[0])
print()
print(CSN_data[-1])

# %% [markdown]
# # Funcom

# %%
from original_data.funcom_processed.load import load


# %%
print(load)


# %%
src, com = load()


# %%
print(type(src))
print(type(com))


# %%
print(list(src.keys())[0])
print(src['321'])
print(com['321'])


# %%
funcom_empty = 0
funcom_Avoid = {}
funcom_Dup = 0
funcom_error = 0

FunCom_data = []
keys = list(src.keys())


# %%
for idx in range(len(keys)):
    if idx % 100000 == 0:
        print(datetime.datetime.now(), ":", idx)

    key = str(keys[idx])
    
    out_dict = {}
    out_dict['src'] = 'FunCom'
    out_dict['src_div'] = "none"
    out_dict['src_idx'] = idx
        
    out_dict['original_code'] = src[key].strip()
    out_dict['original_nl'] = com[key].strip()

    try:
        out_dict['code'] = code_filter(out_dict['original_code'], code_filter_flags).strip()
        out_dict['nl'] = nl_filter(out_dict['original_nl'], nl_filter_flags).strip()

        check_str = out_dict['code']+SEPARATOR+out_dict['nl']

        try:
            mystr = funcom_Avoid[check_str]
            funcom_Dup += 1
            continue
        except KeyError:
            if out_dict['nl'] == "" or out_dict['code'] == "":
                funcom_empty += 1
            else:
                FunCom_data.append(out_dict)
            funcom_Avoid[check_str] = 1
    except:
        funcom_error += 1
    


# %%
print(len(FunCom_data)) # 2138491
print(FunCom_data[0].keys())
print(FunCom_data[-1])


# %%
print("TOTAL =", len(FunCom_data)+funcom_Dup+funcom_empty+funcom_error) # 2149121
print("Duplicate =", funcom_Dup) # 5872
print("Empty =", funcom_empty) # 3826
print("Error =", funcom_error) # 932


# %%
with open(DATA_FOLDER+"FunCom_Data.json", 'w') as outfile:
    json.dump(FunCom_data, outfile)
    outfile.close()
    


# %%
del src
del com
del FunCom_data
gc.collect()


# %%
funcom_file = open(DATA_FOLDER+"FunCom_Data.json", 'r')
FunCom_data = json.load(funcom_file)
funcom_file.close()


# %%
print(len(FunCom_data)) # 2138491


# %%
print(FunCom_data[0].keys())
print(FunCom_data[0])
print()
print(FunCom_data[-1])

# %% [markdown]
# # DeepCom

# %%
INPUT_FOLDER = DATA_FOLDER+"DeepCom/"
divs = ["test", "valid", "train"]


# %%
DeepCom_empty = 0
DeepCom_Avoid = {}
DeepCom_Dup = 0
DeepCom_error = 0

DeepCom_data = []


# %%
for div in divs:
    
    in_file = open(INPUT_FOLDER+div+".json", 'r')
    in_lines = in_file.readlines()
    in_file.close()
        
    for idx in range(len(in_lines)) :  
        if idx % 100000 == 0:
            print(datetime.datetime.now(), ":", div, idx)   

        sample = json.loads(in_lines[idx])
        out_dict = {}

        out_dict['src'] = 'DeepCom'
        out_dict['src_div'] = div
        out_dict['src_idx'] = idx
        
        out_dict['original_code'] = sample['code'].strip()
        out_dict['original_nl'] = sample['nl'].strip()

        try:
            out_dict['code'] = code_filter(out_dict['original_code'], code_filter_flags).strip()
            out_dict['nl'] = nl_filter(out_dict['original_nl'], nl_filter_flags).strip()

            check_str = out_dict['code']+SEPARATOR+out_dict['nl']

            try:
                mystr = DeepCom_Avoid[check_str]
                DeepCom_Dup += 1
                continue
            except KeyError:
                if out_dict['nl'] == "" or out_dict['code'] == "":
                    DeepCom_empty += 1
                else:
                    DeepCom_data.append(out_dict)
                DeepCom_Avoid[check_str] = 1
        except:
            DeepCom_error += 1
        
        


# %%
print(len(DeepCom_data)) # 469039
print(DeepCom_data[0].keys())
print(DeepCom_data[-1])


# %%
print("TOTAL =", len(DeepCom_data)+DeepCom_Dup+DeepCom_empty+DeepCom_error) # 588108
print("Duplicate =", DeepCom_Dup) # 118806
print("Empty =", DeepCom_empty) # 263
print("Error =", DeepCom_error) # 0


# %%
with open(DATA_FOLDER+"DeepCom_Data.json", 'w') as outfile:
    json.dump(DeepCom_data, outfile)
    outfile.close()
    


# %%
del in_lines
del DeepCom_data
gc.collect()


# %%
DeepCom_file = open(DATA_FOLDER+"DeepCom_Data.json", 'r')
DeepCom_data = json.load(DeepCom_file)
DeepCom_file.close()


# %%
print(len(DeepCom_data)) # 469039


# %%
print(DeepCom_data[0].keys())
print(DeepCom_data[0])
print()
print(DeepCom_data[-1])

# %% [markdown]
# # CONCODE

# %%
INPUT_FOLDER = DATA_FOLDER+"concode/"
divs = ["test", "valid", "train"]


# %%
CONCODE_empty = 0
CONCODE_Avoid = {}
CONCODE_Dup = 0
CONCODE_error = 0

CONCODE_data = []


# %%
for div in divs:
    print(div, end=' : ')
    
    in_file = open(INPUT_FOLDER+div+"_shuffled_with_extra.json", 'r')
    in_lines = in_file.readlines()
    in_file.close()
        
    print("File read complete")
    
    for idx in range(len(in_lines)) :
        if idx % 100000 == 0:
            print(datetime.datetime.now(), ":", div, idx)        
    
        sample = json.loads(in_lines[idx])
        out_dict = {}

        out_dict['src'] = 'CONCODE'
        out_dict['src_div'] = div
        out_dict['src_idx'] = idx
        
        out_dict['original_code'] = ' '.join(sample['code']).strip()
        out_dict['original_nl'] = sample['nl'].strip()

        try:
            out_dict['code'] = code_filter(out_dict['original_code'], code_filter_flags).strip()
            out_dict['nl'] = nl_filter(out_dict['original_nl'], nl_filter_flags).strip()

            check_str = out_dict['code']+SEPARATOR+out_dict['nl']

            try:
                mystr = CONCODE_Avoid[check_str]
                CONCODE_Dup += 1
                continue
            except KeyError:
                if out_dict['nl'] == "" or out_dict['code'] == "":
                    CONCODE_empty += 1
                else:
                    CONCODE_data.append(out_dict)
                CONCODE_Avoid[check_str] = 1
        except:
            CONCODE_error += 1
    
    del in_lines
    gc.collect()
        


# %%
print(len(CONCODE_data)) # 733878
print(CONCODE_data[0].keys())
print(CONCODE_data[-1])


# %%
print("TOTAL =", len(CONCODE_data)+CONCODE_Dup+CONCODE_empty+CONCODE_error) # 2184310
print("Duplicate =", CONCODE_Dup) # 1425320
print("Empty =", CONCODE_empty) # 24751
print("Error =", CONCODE_error) # 361


# %%
with open(DATA_FOLDER+"CONCODE_Data.json", 'w') as outfile:
    json.dump(CONCODE_data, outfile)
    outfile.close()
    


# %%
del CONCODE_data
gc.collect()


# %%
CONCODE_file = open(DATA_FOLDER+"CONCODE_Data.json", 'r')
CONCODE_data = json.load(CONCODE_file)
CONCODE_file.close()


# %%
print(len(CONCODE_data)) # 733878


# %%
print(CONCODE_data[0].keys())
print(CONCODE_data[0])
print()
print(CONCODE_data[-1])

# %% [markdown]
# # CodeSearchNet-Py2Java

# %%
INPUT_FOLDER = DATA_FOLDER+"CSN_Python_to_Java/"
INPUT_FILE = INPUT_FOLDER+"CSN_Python_to_Java.json"


# %%
in_file = open(INPUT_FILE, 'r')
in_data = json.load(in_file)
in_file.close()


# %%
print(type(in_data))
print(len(in_data))


# %%
print(in_data[0].keys())
print(in_data[0])


# %%
print(type(in_data[0]['truncated']))


# %%
CSN_Py2Java_empty = 0
CSN_Py2Java_Avoid = {}
CSN_Py2Java_Dup = 0
CSN_Py2Java_error = 0

CSN_Py2Java_data = []


# %%
for idx in range(len(in_data)):
    if idx % 100000 == 0:
        print(datetime.datetime.now(), ":", idx)

    sample = in_data[idx]
    out_dict = {}

    out_dict['src'] = 'CodeSearchNet-Py2Java'
    
    if sample['truncated']:
        out_dict['src_div'] = 'truncated'
    else:
        out_dict['src_div'] = 'full'
        
    out_dict['src_idx'] = idx
        
    out_dict['original_code'] = sample['converted_code'].strip()
    out_dict['original_nl'] = sample['docstring'].strip()

    try:
        out_dict['code'] = code_filter(out_dict['original_code'], code_filter_flags).strip()
        out_dict['nl'] = nl_filter(out_dict['original_nl'], nl_filter_flags).strip()

        check_str = out_dict['code']+SEPARATOR+out_dict['nl']

        try:
            mystr = CSN_Py2Java_Avoid[check_str]
            CSN_Py2Java_Dup += 1
            continue
        except KeyError:
            if out_dict['nl'] == "" or out_dict['code'] == "":
                CSN_Py2Java_empty += 1
            else:
                CSN_Py2Java_data.append(out_dict)
            CSN_Py2Java_Avoid[check_str] = 1
    except:
        CSN_Py2Java_error += 1


# %%
print(len(CSN_Py2Java_data)) # 434032
print(CSN_Py2Java_data[0].keys())
print(CSN_Py2Java_data[0])


# %%
print("TOTAL =", len(CSN_Py2Java_data)+CSN_Py2Java_Dup+CSN_Py2Java_empty+CSN_Py2Java_error) # 456000
print("Duplicate =", CSN_Py2Java_Dup) # 98
print("Empty =", CSN_Py2Java_empty) # 702
print("Error =", CSN_Py2Java_error) # 21168


# %%
with open(DATA_FOLDER+"CSN_Py2Java_Data.json", 'w') as outfile:
    json.dump(CSN_Py2Java_data, outfile)
    outfile.close()


# %%
del in_data
del CSN_Py2Java_data
gc.collect()


# %%
CSN_Py2Java_file = open(DATA_FOLDER+"CSN_Py2Java_Data.json", 'r')
CSN_Py2Java_data = json.load(CSN_Py2Java_file)
CSN_Py2Java_file.close()


# %%
print(len(CSN_Py2Java_data)) # 


# %%
print(CSN_Py2Java_data[0].keys())
print(CSN_Py2Java_data[0])
print()
print(CSN_Py2Java_data[-1])

# %% [markdown]
# # Merge the Files

# %%
OUT_FOLDER = 'data/CoDesc/'
if not os.path.exists(OUT_FOLDER):
    os.mkdir(OUT_FOLDER)
    
files = ["CSN_Data.json", "FunCom_Data.json", "DeepCom_Data.json", "CONCODE_Data.json", "CSN_Py2Java_Data.json"]


# %%
out_data = []
out_id = 0

avoid_dict = {}
dup_removed = 0

partiton2id_dict = {}
partiton2id_dict['train'] = []
partiton2id_dict['valid'] = []
partiton2id_dict['test'] = []


src2id_dict = {}
src2id_dict['CodeSearchNet-Java'] = {}
src2id_dict['CodeSearchNet-Java']['test'] = []
src2id_dict['CodeSearchNet-Java']['valid'] = []
src2id_dict['CodeSearchNet-Java']['train'] = []
src2id_dict['CodeSearchNet-Java']['removed'] = []
src2id_dict['CodeSearchNet-Java']['ALL'] = []

src2id_dict['FunCom'] = {}
src2id_dict['FunCom']['none'] = []
src2id_dict['FunCom']['ALL'] = []

src2id_dict['DeepCom'] = {}
src2id_dict['DeepCom']['test'] = []
src2id_dict['DeepCom']['valid'] = []
src2id_dict['DeepCom']['train'] = []
src2id_dict['DeepCom']['ALL'] = []

src2id_dict['CONCODE'] = {}
src2id_dict['CONCODE']['test'] = []
src2id_dict['CONCODE']['valid'] = []
src2id_dict['CONCODE']['train'] = []
src2id_dict['CONCODE']['ALL'] = []

src2id_dict['CodeSearchNet-Py2Java'] = {}
src2id_dict['CodeSearchNet-Py2Java']['full'] = []
src2id_dict['CodeSearchNet-Py2Java']['truncated'] = []
src2id_dict['CodeSearchNet-Py2Java']['ALL'] = []



# %%
for filename in files:
    print(filename, end=" : ")
    
    in_file = open(DATA_FOLDER+filename, 'r')
    in_data = json.load(in_file)
    in_file.close()
    
    print("File load complete.")
    
    for sample in in_data:
        check_str = sample['code']+SEPARATOR+sample['nl']
        try:
            mystr = avoid_dict[check_str]
            dup_removed += 1
            continue
        except:
            avoid_dict[check_str] = 1
            
            out_dict = {}
            out_dict['id'] = out_id
            src2id_dict[sample['src']][sample['src_div']].append(out_id)
            src2id_dict[sample['src']]['ALL'].append(out_id)
            out_id += 1

            out_dict.update(sample)
            out_data.append(out_dict)    
        
        
    del in_data
    gc.collect()
        

# %%
print("DUPLICATE REMOVED =", dup_removed) # 54093
print("REMAINING DATAPOINTS =", len(out_data)) # 4211516
print(out_data[0].keys())
print(out_data[-1])


# %%
# create paritions
random.seed(datetime.datetime.now().microsecond)
TEST_RATIO = 0.1
VALID_RATIO = 0.1

for src in ['CodeSearchNet-Java', 'FunCom', 'DeepCom', 'CONCODE', 'CodeSearchNet-Py2Java']:
    ids = src2id_dict[src]['ALL']
    random.shuffle(ids)
    
    num_test = int(len(ids)*TEST_RATIO)
    num_valid = int(len(ids)*VALID_RATIO)
    test_ids = ids[0:num_test]
    valid_ids = ids[num_test:num_test+num_valid]
    train_ids = ids[num_test+num_valid:]
    
    partiton2id_dict['train'].extend(train_ids)
    partiton2id_dict['valid'].extend(valid_ids)
    partiton2id_dict['test'].extend(test_ids)
    
    


# %%
print(len(partiton2id_dict['train'])) # 3369218
print(len(partiton2id_dict['valid'])) # 421149
print(len(partiton2id_dict['test'])) # 421149


# %%
for div in ['train', 'valid', 'test']:
    for idx in partiton2id_dict[div]:
        out_data[idx]['partition'] = div


# %%
with open(OUT_FOLDER+"CoDesc.json", 'w') as outfile:
    json.dump(out_data, outfile, indent=2)
    outfile.close()


# %%
print(len(src2id_dict['DeepCom']['test']))
# print(src2id_dict['DeepCom']['test'])

print(len(src2id_dict['CONCODE']['test']))
# print(src2id_dict['CONCODE']['test'])


# %%
with open(OUT_FOLDER+"partiton2id_dict.json", 'w') as outfile:
    json.dump(partiton2id_dict, outfile, indent=2)
    outfile.close()


# %%
with open(OUT_FOLDER+"src2id.json", 'w') as outfile:
    json.dump(src2id_dict, outfile, indent=2)
    outfile.close()


# %%
#Save id to source mapping

for idx in range(len(out_data)):
    out_data[idx].pop('code')
    out_data[idx].pop('nl')
    out_data[idx].pop('original_nl')
    out_data[idx].pop('original_code')

id2src_df = pd.DataFrame(out_data)
id2src_df.to_csv(OUT_FOLDER+"id2src.csv", index=False)


# %%
#Save source lenghts
src_len = []


src_len.append(['CodeSearchNet-Java', 'test', str(len(src2id_dict['CodeSearchNet-Java']['test']))])
src_len.append(['CodeSearchNet-Java', 'valid', str(len(src2id_dict['CodeSearchNet-Java']['valid']))])
src_len.append(['CodeSearchNet-Java', 'train', str(len(src2id_dict['CodeSearchNet-Java']['train']))])
src_len.append(['CodeSearchNet-Java', 'removed', str(len(src2id_dict['CodeSearchNet-Java']['removed']))])
src_len.append(['CodeSearchNet-Java', 'ALL', str(len(src2id_dict['CodeSearchNet-Java']['ALL']))])

src_len.append(['FunCom', 'none', str(len(src2id_dict['FunCom']['none']))])
src_len.append(['FunCom', 'ALL', str(len(src2id_dict['FunCom']['ALL']))])

src_len.append(['DeepCom', 'test', str(len(src2id_dict['DeepCom']['test']))])
src_len.append(['DeepCom', 'valid', str(len(src2id_dict['DeepCom']['valid']))])
src_len.append(['DeepCom', 'train', str(len(src2id_dict['DeepCom']['train']))])
src_len.append(['DeepCom', 'ALL', str(len(src2id_dict['DeepCom']['ALL']))])

src_len.append(['CONCODE', 'test', str(len(src2id_dict['CONCODE']['test']))])
src_len.append(['CONCODE', 'valid', str(len(src2id_dict['CONCODE']['valid']))])
src_len.append(['CONCODE', 'train', str(len(src2id_dict['CONCODE']['train']))])
src_len.append(['CONCODE', 'ALL', str(len(src2id_dict['CONCODE']['ALL']))])

src_len.append(['CodeSearchNet-Py2Java', 'full', str(len(src2id_dict['CodeSearchNet-Py2Java']['full']))])
src_len.append(['CodeSearchNet-Py2Java', 'truncated', str(len(src2id_dict['CodeSearchNet-Py2Java']['truncated']))])
src_len.append(['CodeSearchNet-Py2Java', 'ALL', str(len(src2id_dict['CodeSearchNet-Py2Java']['ALL']))])

src_len.append(['ALL', 'ALL', str(len(out_data))])

src_len_df = pd.DataFrame(src_len, columns = ['src', 'src_div', 'len'])
src_len_df.to_csv(OUT_FOLDER+"src_len.csv", index=False)


