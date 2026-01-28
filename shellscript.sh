#!/bin/bash
#check virrtual enivorment
if [ -d "venv" ]; then
    echo " using venv enviroment"
    source venv/bin/activate
else
    echo "venv not found"
    echo "create it first"
    exit 1
fi
echo "intalling teh packages"
pip install -r requirements.txt

echo " running teh flask application"
python app/__init__.py

