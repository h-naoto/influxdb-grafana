FROM centos

MAINTAINER hanaue.naoto@po.ntts.co.jp

WORKDIR /root

RUN yum install -y wget pycrypto

RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py


ADD ./collect.py /root/

RUN pip install Fabric influxdb

CMD ["python", "collect.py"]
