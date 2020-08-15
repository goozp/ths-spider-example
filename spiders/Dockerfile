FROM python:3.7

# Set Timezone
ARG TZ=UTC
ENV TZ ${TZ}
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir /code
ADD . /code/
RUN mv /code/sources.list /etc/apt/sources.list

RUN apt-get update \ 
    && apt-get install -y nodejs

WORKDIR /code
RUN pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

CMD ["python", "./main.py"]
