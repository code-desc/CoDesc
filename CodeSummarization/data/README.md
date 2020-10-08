## Dataset link:

Data source: https://drive.google.com/file/d/14nHVljNMb37-tpOW59NaDY26T6z2BcXD/view?usp=sharing

## training procedure
1. Install the required library from requirements.txt file inside `CodeSummarization` directory (pip install requirements.txt).
2. Download the data source from above link. Then extract the zip file inside data/java.
3. Start training from scripts/java/transformer.sh 
run this command 
```bash
 transformer.sh 0 CoDescSum
 ```
4. After two epoch terminate the terminal.
5. Rename 'train' folder to 'pretrain' and rename 'finetune' to 'train'
6. Run this again
```bash
 transformer.sh 0 CoDescSum
 ```
