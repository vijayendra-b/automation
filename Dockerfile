FROM python:3.10-alpine3.16
RUN apk add curl jq
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python && apk add unzip && apk add bash bash-completion coreutils file grep openssl openssh nano sudo tar xz
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

RUN apk add --no-cache --upgrade bash
RUN python -m pip install tk-tools

RUN apk add openjdk8
ENV PATH $PATH:/usr/lib/jvm/java-1.8-openjdk/bin:/usr/bin

RUN mkdir ./allure
RUN wget https://github.com/allure-framework/allure2/releases/download/2.20.1/allure-2.20.1.zip
RUN unzip allure-2.20.1.zip -d ./allure
RUN rm allure-2.20.1.zip
ENV PATH="./allure/allure-2.20.1/bin:${PATH}"

WORKDIR /usr/automation
ADD . .

RUN pip install -r requirements.txt

USER 2000:2000

ADD healthcheck.sh healthcheck.sh

# Differrent options needed for debugging purposes
#ENTRYPOINT ["/bin/bash"]
#ENTRYPOINT ["pytest --alluredir=allure_report/ testcases"]
#ENTRYPOINT ["pytest --alluredir=allure_report/ testcases/teammanagepage/test_tourpoints_when_members_in_team.py"]
#ENTRYPOINT ["pytest"]

ENTRYPOINT sh healthcheck.sh
