## Dataset link:

Data source: https://drive.google.com/file/d/14nHVljNMb37-tpOW59NaDY26T6z2BcXD/view?usp=sharing

## training procedure
1. Download the data source from above link. Then extract the zip file inside `CodeSummarization/data/java/` folder.
2. Start training from `CodeSummarization/scripts/java/transformer.sh`.    
run this command. 
```bash
 transformer.sh 0 CoDescSum
 ```
3. After two epoch terminate the terminal.
4. Rename 'train' folder to 'pretrain' and rename 'finetune' to 'train' inside `CodeSummarization/data/java/`.
5. Run this again.
```bash
 transformer.sh 0 CoDescSum
 ```
