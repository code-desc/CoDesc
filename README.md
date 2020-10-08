# CoDesc

A large dataset of 4.2m Java source code and parallel data of their description from code search, and code summarization studies.

This is the public release of code, and data of our paper titled "CoDesc: Large Code-Description Parallel Dataset", submitted to EACL, 2021.

**Table of Contents**

<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Quickstart](#quickstart)
- [Introduction](#introduction)
- [CoDesc Dataset](#codesc-dataset)
    - [Python to Java Translation](#python-to-java-translation)
    - [CoDesc Dataset Creation](#codesc-dataset-creation)
    - [Preprocess CoDesc for Code Search](#preprocess-codesc-for-code-search)
    - [Preprocess CoDesc for Code Summarization](#preprocess-codesc-for-code-summarization)
- [Tokenizer](#tokenizer)
- [Code Search](#code-search)
- [Code Summarization](#code-summarization)
- [Licenses](#licenses)

<!-- /TOC -->

# Quickstart
  ```bash
  # clone this repository
  git clone https://github.com/code-desc/CoDesc.git
  
  # change permission of scripts
  sudo chmod -R +x CoDesc
  cd CoDesc/

  # setup
  ./Setup/setup.sh
  ```

# Introduction
CoDesc is a noise removed, large parallel dataset of source codes and corresponding natural language descriptions. This dataset is procured from several similar, but noisy datasets including [CodeSearchNet](https://github.com/github/CodeSearchNet.git), [FunCom](http://leclair.tech/data/funcom/), [DeepCom](https://github.com/xing-hu/DeepCom.git), and [CONCODE](https://github.com/sriniiyer/concode.git). We have developed and released the noise removal and preprocessing source codes along with the dataset. We also demonstrate the usefulness of CoDesc dataset in two popular tasks: natural language code search and source code summarization.


# CoDesc Dataset
After initial setup described at [Quickstart](#quickstart), our dataset will be downloaded at `data/` folder along with preprocessed data for code search task and code summarization task. We also provide the source datasets here. Following are the links and descriptions of the dataset and preprocessed data.

1. [CoDesc](https://mega.nz/file/x5BQGDCY#LwmKDu5eYNTdG85xrW85jh3gcJvcsBpKwY9ufTFM1vs): This file contains our 4.2m dataset. The details of this dataset is given in our paper as well as in [Dataset Description](https://github.com/code-desc/CoDesc/blob/master/Dataset%20Description.md) page.

2. [Original_data](https://mega.nz/file/ZpoBla5a#qeSxMXP6v-2FEI237cIVrFhuqnq5DHh88_EKuReSY3k): This file contains the source data from where we have collected and preprocessed our 4.2m dataset.

3. [CSN_preprocessed_data](https://mega.nz/file/Q4oxQCIb#CT7P5zq1WbiWOLTeafg-mFD2QZEmF1YwZmDhGZkzU90): This file contains the preprocessed data for CodeSearchNet challenge. Here test and validation sets are the preprocessed datapoints from CodeSearchNet original test and validation sets.

4. [CSN_preprocessed_data_balanced_partition](https://mega.nz/file/t543VCyA#4BLjB28yYNDT9kXBs6NWmY1ADOCMyuvqDXLg9yPhiaI): This file contains the preprocessed data for CodeSearchNet networks. Here train, test, and validation sets are from our balanced partition described in our paper

5. [NCS_preprocessed_data](https://mega.nz/file/45BXRSSb#sj2bSC9AHxralmpAud6Uy1_g6HOFnZq0Dk4pfqiP-1M): This file contains the preprocessed data for neural code summarization networks.

6. *** add bpe tokenized ncs preprocessed data here ***

## Python to Java Translation
We have created a forked repository of [Transcoder](https://github.com/code-desc/TransCoder.git) that facillicates parallel translation of source codes and speeds up the process by 16 times. Instructions to use Transcoder can be found in the above mentioned repository. The original work is published under the title ["Unsupervised Translation of Programming Languages"](https://arxiv.org/abs/2006.03511).

## CoDesc Dataset Creation
As we have already mentioned, we have provided the original data from sources to the `data/original_data/` folder. To create the 4.2m CoDesc dataset from original data, the following command should be used.
 ```bash
 python Dataset_Preparation/Merge_Datasets.py
 ```

## Preprocess CoDesc for Code Search 
The following command preprocesses CoDesc dataset for [CodeSearchNet](https://arxiv.org/abs/1909.09436) Challenge. It also preprocesses their validation and test sets using the filters defined in our paper.
 ```bash
 python Dataset_Preparation/Preprocess_CSN.py
 ```

 To create a balanced train-valid-test split for CodeSearchNet networks, the command can be used.
  ```bash
 python Dataset_Preparation/Preprocess_CSN_Balanced_Partition.py
 ```

## Preprocess CoDesc for Code Summarization
The following command preprocesses CoDesc dataset for [NeuralCodeSum](https://arxiv.org/abs/2005.00653) networks.
  ```bash
 python Dataset_Preparation/Preprocess_NCS.py
 ```
 
# Tokenizer
if huggingface tokenizer library is not installed run this command
  ```bash
 pip install transformers
 ```
 to train and create tokenized files using bpe use this command
 ```bash
 python Tokenizer/huggingface_bpe.py
 ```

The tokenizers for source codes and natural language descriptions are given in the `Tokenizer/` directory. To use the tokenizers in python, `code_filter` and `nl_filter` functions will have to be imported from `Tokenizer/CodePreprocess_final.py` and `Tokenizer/NLPreprocess_final.py`.  Moreover, two json files named `code_filter_flag.json` and `nl_filter_flag.json` containing the options to preprocess code and description data will have to be present in the working directory. These two files must follow the formats given the `Tokenizer/` folder. These flag options are also briefly described in the above mentioned json files.

# Code Search
During the initial setup described at [Quickstart](#quickstart), a forked version of [CodeSearchNet](https://github.com/code-desc/CodeSearchNet.git) is cloned into the working directory, and the preprocessed data of CoDesc will be copied to `CodeSearchNet/resources/data/` directory. To use the preprocessed dataset of balanced partition, clear the above mentioned folder, and copy the content inside of `data/csn_preprocessed_data_balanced_partition/` into it.

Then the following commands will train and test code search networks:
 ```bash
 cd CodeSearchNet/
 
 script/console
 wandb login
 
 python train.py --model neuralbowmodel --run-name nbow_CoDesc
 python train.py --model rnnmodel --run-name rnn_CoDesc
 python train.py --model selfattentionmodel --run-name attn_CoDesc
 python train.py --model convolutionalmodel --run-name conv_CoDesc
 python train.py --model convselfattentionmodel --run-name convattn_CoDesc
 ```

# Code Summarization
We used the original implementation of Code Summarization. [NeuralCodeSum](https://github.com/wasiahmad/NeuralCodeSum.git)


# Licenses
Codes, dataset and models from [CodeSearchNet](https://github.com/github/CodeSearchNet.git), and [NeuralCodeSum](https://github.com/wasiahmad/NeuralCodeSum.git) are used with the licenses provided at their respective repositories.   
These codes, dataset, and preprocessed data are released under the [MIT license](https://github.com/code-desc/CoDesc/blob/master/LICENSE).
