FROM python:3.11-bookworm

COPY requirements.txt /app/build/requirements.txt

RUN apt-get update

RUN pip install uv
RUN uv venv /etc/venv
ENV VIRTUAL_ENV=/etc/venv
ENV PATH="/etc/venv/bin:$PATH"
RUN uv pip install -r /app/build/requirements.txt

COPY main.py /app/src/main.py

WORKDIR /app/src

EXPOSE 4445
RUN chmod +x /etc/venv/bin/activate
RUN /etc/venv/bin/activate

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4445", "--workers", "4"]
