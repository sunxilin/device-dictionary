FROM python:3.11.3

COPY requirements.txt requirements.txt

RUN python3 -m pip install --upgrade pip setuptools requests -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN python3 -m pip install -r requirements.txt

COPY . .

CMD [ "make", "webserver"]