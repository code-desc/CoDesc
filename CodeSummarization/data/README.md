## Dataset link:

Data source: https://drive.google.com/file/d/1KfrWmo90Y7EPbMAniS3QB1zxYYiZVgMP/view?usp=drivesdk

## training procedure
1. Extract the zip file in data/java
2. Start training from scripts/java/transformer.sh 
run this command 
```bash
 transformer.py 0 fullrun
 ```
3. After two epoch terminate the terminal.
4. Rename 'train' folder to 'pretrain' and rename 'finetune' to 'train'
5. Run this again
```bash
 transformer.py 0 fullrun
 ```
