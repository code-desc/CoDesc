# Details of CodeCorpus
  
## File description
[CodeCorpus](https://mega.nz/file/Rsx3zaqY#stMEpCe33JLAIcslPZRf6sKXcka3JW3eivgjR5DFl5U) contains the follwing files that consists the 4.2m dataset and related information.  

1. CodeCorpus.json:  
    * List of python dictionaries type  
    * Each entry has the following keys:  
        - id: unique id in CodeCorpus dataset  
        - src: source dataset  
        - src_div: which subset the entry was taken from, e.g. train, test, etc.  
        - src_idx: idx in source subset  
        - code: java function  
        - nl: natural language description after initial filtering  
        - original_code: source code taken from source  
        - original_nl: natural language description taken from source  
        - partition: 'train', 'valid' or 'test'  
  
2. src2id.json:  
	* Dictionary type  
	* src2id[src][src_div] is a list of ids from CodeCorpus dataset  
	* src -> src_div:   
		- "CodeSearchNet-Java" -> "test", "valid", "train", "removed"  
		- "FunCom" -> "none"   
		- "DeepCom" -> "test", "valid", "train"  
		- "CONCODE" -> "test", "valid", "train"   
		- "CodeSearchNet-Py2Java" -> "full", "truncated"  
  
3. id2src.csv:  
	* csv type  
	* Columns:   
		- id: unique id in CodeCorpus dataset  
		- src: source dataset  
		- src_div: which subset the entry was taken from, e.g. train, test, etc.  
		- src_idx: idx in source subset   
  
4. src_len.csv  
	* csv type  
	* Columns:  
		- src: source dataset  
		- src_div: which subset the entry was taken from, e.g. train, test, etc.  
		- len: number of datapoints under this subset  
  
5. partition2id.json  
	* Dictionary type  
	* partition2id['train'], partition2id['valid'], and partition2id['test'] are list of ids in CodeCorpus dataset corresponding to the partition they belong to.  
