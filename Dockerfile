# first stage
FROM python:3.8 AS builder
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
# install dependencies
RUN pip install --user -r requirements.txt


FROM python:3.8-slim
WORKDIR /code
COPY --from=builder /root/.local/bin /root/.local
COPY ./src .
ENV PATH="/opt/venv/bin:$PATH"

CMD [ "python", "./capture.py"  ]
