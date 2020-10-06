from mega import Mega
import os

# go to data folder where we will keep the data
os.chdir('data/')


print('Starting download...')
mega = Mega()

mega.download_url('')  
print("CodeCorpus.7z downloaded")
os.system("7z x CodeCorpus.7z")

mega.download_url('')  
print("csn_preprocessed_data.7z downloaded")
os.system("7z x csn_preprocessed_data.7z")

mega.download_url('')  
print("csn_preprocessed_data_balanced_partition.7z downloaded")
os.system("7z x csn_preprocessed_data_balanced_partition.7z")

mega.download_url('')  
print("ncs_preprocessed_data.7z downloaded")
os.system("7z x ncs_preprocessed_data.7z")

mega.download_url('')  
print("original_data.7z downloaded")
os.system("7z x original_data.7z")


# go back to previous folder
os.chdir('..')



