#/usr/bin/bash
base_dir="/home/zacharygibbs/documents/dataengineering/wordlescraper/wordlescraper"
cd $base_dir
if [ $# -eq 0 ]
  then
    echo "Running in Current Python Env"
    python workup.py
elif [ $# -eq 1 ]
  then
    echo "Running in Conda Env $1"
    conda run -n $1 workup.py
else
    echo "Running in Conda Env $1:$2"
    $1 run -n $2 python workup.py 1>> log.txt 2>> log.txt 
fi

