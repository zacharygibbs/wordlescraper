#/usr/bin/bash

if [ $# -eq 0 ]
  then
    echo "Running in Current Python Env"
    python get_tweets.py
    python get_wordlist.py
    python get_allwords.py
    python merge.py
    python send_ftp.py
else
    echo "Running in Conda Env $1"
    conda run -n $1 python get_tweets.py
    conda run -n $1 python get_wordlist.py
    conda run -n $1 python get_allwords.py
    conda run -n $1 python merge.py
    conda run -n $1 python send_ftp.py
fi

