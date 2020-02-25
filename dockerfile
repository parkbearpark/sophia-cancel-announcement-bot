FROM joyzoursky/python-chromedriver:latest
WORKDIR /usr/work/
COPY ./*  /usr/work/
RUN ["pip", "install", "--upgrade", "pip"]
RUN ["pip", "install", "-r", "requirements.txt"]
COPY  ./src /usr/work/
CMD ["python", "__main__.py"]
