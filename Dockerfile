FROM redbutterfly/meinheld-gunicorn-project:v0.1.0
LABEL maintainer="Han Fei <hanfei1009@163.com>"

COPY ./project/config/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com

COPY ./project /project
COPY ./.env /project
WORKDIR /project/

