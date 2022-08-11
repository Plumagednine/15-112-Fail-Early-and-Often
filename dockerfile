# Dockerfile, Image, Container

FROM python:3.9.13

# ADD . ./

# ADD /gameData ./gameData
# ADD /monsterSprites ./monsterSprites
# ADD /textures ./textures
# ADD /characterSprites ./characterSprites
# ADD /font ./font

WORKDIR /15-112-Fail-Early-and-Often

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN apt-get update -y

RUN apt-get install tk -y

ADD . .

CMD [ "python", "Main.py" ]
