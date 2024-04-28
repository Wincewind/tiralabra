FROM ubuntu:22.04

WORKDIR /usr/src/app
#Install curl, python and poetry
RUN apt-get update && apt-get install -y curl python3
RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

# Copy only dependency info
COPY poetry.lock ./
COPY pyproject.toml ./

#Install dependencies
RUN poetry update && poetry install

# Copy files
COPY . .

# Replacing CMD with ENTRYPOINT
ENTRYPOINT ["poetry", "run", "python3", "src/main.py"]
