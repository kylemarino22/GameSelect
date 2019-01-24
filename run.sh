if [ -e GameSelect.egg-info ]
then
    echo "egg-info exists"
else
    echo "egg-info does not exist"
    pip install -e . &>log.txt
fi
export FLASK_ENV=development
export FLASK_APP=src/main.py
flask run
