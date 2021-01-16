# setup
sudo apt install mecab libmecab-dev mecab-ipadic-utf8

sudo apt install git make curl xz-utils file
cd /tmp
git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
cd mecab-ipadic-neologd
./bin/install-mecab-ipadic-neologd -n

sudo apt install ffmpeg