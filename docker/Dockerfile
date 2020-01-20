FROM balenalib/raspberrypi3-debian:stretch

RUN [ "cross-build-start" ]
#RUN apk add --update --no-cache py3-numpy py3-setuptools py3-pillow py3-paho-mqtt python3-dev
RUN apt-get update && apt-get install python3-numpy python3-setuptools python3-pil python3-sense-hat python3-pip

ADD . ./
RUN pip3 install -r requirements.txt

RUN [ "cross-build-end" ]

CMD ["python3", "main.py"]
#CMD ["sleep", "6000"]

