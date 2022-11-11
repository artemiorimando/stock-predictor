FROM python:3.8

WORKDIR .

RUN apt-get -y update && apt-get install -y \
    python3-dev \
    apt-utils \
    python-dev \
    build-essential && rm -rf /var/lib/apt/lists/*

RUN apt-get install g++ gcc

RUN pip install --no-cache-dir -U pip
RUN pip install --no-cache-dir -U cython
RUN pip install --no-cache-dir -U numpy
RUN pip install --no-cache-dir -U pystan==2.19.1.1

COPY requirements.txt .
RUN pip install --no-cache-dir -U -r  requirements.txt

COPY src/ .

CMD ["uvicorn", "main:app", "--reload", "--workers", "1", "--host", "0.0.0.0", "--port", "8000"]