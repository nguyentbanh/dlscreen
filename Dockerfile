# first stage
FROM python:3.8 AS builder
#COPY requirements.txt .

# install dependencies
#RUN pip install --user -r requirements.txt
RUN pip install --user click selenium fitz natsort
RUN ls /root/.local/bin
RUN pip show click
RUN pip show selenium

FROM python:3.8-slim
WORKDIR /code

COPY --from=builder /root/.local/bin /root/.local
COPY ./src .
RUN ls /root/.local

ENV PATH=/root/.local:$PATH
RUN echo $PATH

CMD [ "python", "./capture.py"  ]
