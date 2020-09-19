# first stage
FROM python:3.8 AS builder
#COPY requirements.txt .

# install dependencies
#RUN pip install --user -r requirements.txt
RUN pip install --user click selenium fitz natsort

FROM python:3.8-slim
WORKDIR /code

COPY --from=builder /root/.local/bin /root/.local/bin
COPY ./src .

ENV PATH=/root/.local:$PATH

CMD [ "python", "./capture.py"  ]
