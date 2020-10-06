from mega import Mega
import os

# go to data folder where we will keep the data
os.chdir('data/')


print('Starting download...')
mega = Mega()

mega.download_url('https://mega.nz/file/Rsx3zaqY#stMEpCe33JLAIcslPZRf6sKXcka3JW3eivgjR5DFl5U')  
print("CodeCorpus.7z downloaded")
os.system("7z x CodeCorpus.7z")

mega.download_url('https://mega.nz/file/Q4oxQCIb#CT7P5zq1WbiWOLTeafg-mFD2QZEmF1YwZmDhGZkzU90')  
print("csn_preprocessed_data.7z downloaded")
os.system("7z x csn_preprocessed_data.7z")

mega.download_url('https://mega.nz/file/t543VCyA#4BLjB28yYNDT9kXBs6NWmY1ADOCMyuvqDXLg9yPhiaI')  
print("csn_preprocessed_data_balanced_partition.7z downloaded")
os.system("7z x csn_preprocessed_data_balanced_partition.7z")

mega.download_url('https://mega.nz/file/Npo1RaBZ#ug6jJPacpjNht537PmOwxsR2MlOps0Y-LOwhx8lQ5ys')  
print("ncs_preprocessed_data.7z downloaded")
os.system("7z x ncs_preprocessed_data.7z")

mega.download_url('https://mega.nz/file/ZpoBla5a#qeSxMXP6v-2FEI237cIVrFhuqnq5DHh88_EKuReSY3k')  
print("original_data.7z downloaded")
os.system("7z x original_data.7z")


# go back to previous folder
os.chdir('..')



