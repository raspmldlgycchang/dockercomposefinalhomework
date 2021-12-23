FROM ubuntu:20.04
RUN chown root:root /etc/apt/sources.list
RUN chmod 644 /etc/apt/sources.list
RUN sed -i'' 's/archive\.ubuntu\.com/us\.archive\.ubuntu\.com/' /etc/apt/sources.list

RUN apt update && apt install -y openssh-server
RUN apt -y install python3 vim python3-pip
RUN apt -y install wget
RUN apt -y install screen
RUN pip3 install fastapi
RUN pip3 install uvicorn
RUN pip3 install pymongo
RUN pip3 install pymongo[srv]
RUN pip3 install pydantic
RUN wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | apt-key add -
RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.4.list
RUN apt update
RUN apt install -y mongodb

RUN mkdir /var/run/sshd
RUN echo 'root:fdsfsfsfw' | chpasswd
RUN sed -i 's/#*PermitRootLogin prohibit-password/PermitRootLogin yes/g' /etc/ssh/sshd_config

#SSH login fix. Otherwise user is kicked off after login
RUN sed -i 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' /etc/pam.d/sshd

ENV NOTVISIBLE="in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

WORKDIR /root

COPY main.py /root/project/main.py
COPY music-recommendation/recom_data/results/json_dir /root/music-recommendation/recom_data/results
COPY music-recommendation/data/song_meta.json /root/music-recommendation/data/song_meta.json
COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN mkdir -p /root/data/db/
VOLUME ["/data/db/"]

EXPOSE <ssh포트컨테이너>
EXPOSE <uvicorn포트컨테이너>
EXPOSE <몽고디비포트컨테이너>
CMD ["/usr/sbin/sshd", "-D"]
