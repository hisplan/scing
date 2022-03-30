#!/bin/bash

usage()
{
cat << EOF
USAGE: `basename $0` [options]
    -d  directory to search
EOF
}

while getopts "d:h" OPTION
do
    case $OPTION in
        d) search_dir=$OPTARG ;;
        h) usage; exit 1 ;;
        *) usage; exit 1 ;;
    esac
done

if [ -z "$search_dir" ]
then
    usage
    exit 1
fi

find ${search_dir} -name "*.wdl" | xargs -I {} grep -EH "dockerImage|docker:" {} | grep -v "docker: dockerImage" | grep -o '".*"' | sort | uniq

