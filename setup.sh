curdir=$(pwd)
echo "#search arxiv paer at a specific time every day" >>~/.bashrc
echo "echo ${curdir}/search_arxiv.py | at 7:00 2>/dev/null " >>~/.bashrc
source ~/.bashrc
