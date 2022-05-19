#/usr/bin/bash
base_dir="/home/zacharygibbs/Documents/dataengineering/wordlescraper"
cd $base_dir
if [ $# -eq 0 ]
  then
    echo "Running in Current Python Env"
    python get_tweets.py
    python get_wordlist.py
    python get_allwords.py
    python merge.py
    python send_ftp.py
elif [ $# -eq 1 ]
  then
    echo "Running in Conda Env $1"
    conda run -n $1 python get_tweets.py
    conda run -n $1 python get_wordlist.py
    conda run -n $1 python get_allwords.py
    conda run -n $1 python merge.py
    conda run -n $1 python send_ftp.py
else
    echo "Running in Conda Env $1:$2"
    $1 run -n $2 python get_tweets.py 1>> log.txt 2>> log.txt 
    $1 run -n $2 python get_wordlist.py 1>> log.txt 2>> log.txt
    $1 run -n $2 python get_allwords.py 1>> log.txt 2>> log.txt
    $1 run -n $2 python merge.py 1>> log.txt 2>> log.txt
    $1 run -n $2 python send_ftp.py 1>> log.txt 2>>log.txt
fi

