from tokenizers import CharBPETokenizer

tokenizer_code =  CharBPETokenizer()
tokenizer_doc =  CharBPETokenizer()

#tokenizer.train([list of files to learn tokenizer from], vocab_size)
#change file locations if the training files is elsewhere
tokenizer_code.train(["ncs_preprocessed_data/train-ncs/code.original_subtoken", "ncs_preprocessed_data/dev/code.original_subtoken"], vocab_size=100000) 
tokenizer_doc.train(["ncs_preprocessed_data/train-ncs/javadoc.original", "ncs_preprocessed_data/dev/javadoc.original"], vocab_size=100000)

print(tokenizer_code.get_vocab)
print(tokenizer_doc.get_vocab)

#use the trained tokenizer_code to encode and write in output_file 

file_dir = "data/ncs_preprocessed_data/train-CoDesc/"
src_file_name = "code.original_subtoken"
tgt_file_name = "code.bpe"

output_file = open(file_dir+"/"+tgt_file_name, "w")
output_file.close()
output_file = open(file_dir+"/"+tgt_file_name, "a")
with open(file_dir+"/"+src_file_name, 'r') as file:
  for line in file:
    output = tokenizer_code.encode(line)
    line = ' '.join(output.tokens).replace("</w>", "")
    output_file.write(line)
    output_file.write("\n")
output_file.close()


#use the trained tokenizer_doc to encode and write in output_file 

file_dir = "data/ncs_preprocessed_data/train-CoDesc/"
src_file_name = "javadoc.original"
tgt_file_name = "javadoc.bpe"

output_file = open(file_dir+"/"+tgt_file_name, "w")
output_file.close()
output_file = open(file_dir+"/"+tgt_file_name, "a")
with open(file_dir+"/"+src_file_name, 'r') as file:
  for line in file:
    output = tokenizer_doc.encode(line)
    line = ' '.join(output.tokens).replace("</w>", "")
    output_file.write(line)
    output_file.write("\n")
output_file.close()
