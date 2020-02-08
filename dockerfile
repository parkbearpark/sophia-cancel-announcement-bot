FROM joyzoursky/python-chromedriver:3.7-alpine3.8-selenium
WORKDIR /usr/work/
COPY ./*  /usr/work/
RUN [ "pip", "install", ".""]
CMD ["python", "__main__.py"]