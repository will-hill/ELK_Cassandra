# CREATE Virtual Environment w/ Requirements
mkdir -p ~/py_envs/elk_nlp
virtualenv -p python3 ~/py_envs/elk_nlp
source /home/${USER}/py_envs/elk_nlp/bin/activate
python -m pip install -r requirements.txt
