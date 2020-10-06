# setup linux environment
sudo apt-get install curl
sudo apt-get install p7zip

# install docker
./setup/install_docker.sh

# setup python environment
pip install --upgrade pip
pip install mega.py
pip install pandas
pip install numpy
pip install jsonlines
pip install javalang

# download dataset
mkdir data/
python Setup/Download_data.py


# setup CodeSearchNet
git clone https://github.com/code-description2020/CodeSearchNet.git
sudo cp -rf -t CodeSearchNet/resources/data/ data/sample_data/csn_preprocessed_data/java/
cd CodeSearchNet/
script/setup
cd ..


