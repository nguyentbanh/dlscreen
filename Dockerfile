# first stage
#FROM python:3.8 AS builder
#COPY requirements.txt .

# install dependencies
#RUN pip install --user -r requirements.txt
#RUN pip install --user click selenium fitz natsort
#RUN ls /root/.local/bin
#RUN ls /root/.local/lib/python3.8/site-packages

FROM python:3.8-slim
WORKDIR /code
RUN pip install --user click selenium fitz natsort

#COPY --from=builder /root/.local/bin /root/.local
#COPY --from=builder /root/.local/lib/python3.8/site-packages /root/.local
COPY ./src .
RUN ls /root/.local/bin
RUN ls /root/.local/lib/python3.8/site-packages

ENV PATH=/root/.local/bin:$PATH

CMD [ "python", "./capture.py"  ]
