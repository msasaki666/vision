FROM python:3.10
WORKDIR /app
COPY pyproject.toml poetry.lock ./
# hadolint ignore=DL3013
RUN pip install --no-cache-dir -U pip && \
  pip install --no-cache-dir poetry && \
  # poetryはデフォルトでvenvと呼ばれる仮想環境構築機能がオンになっているが, dockerでは必要ないのでoff
  poetry config virtualenvs.create false && \
  poetry install && \
  rm pyproject.toml poetry.lock && \
  # bash補完
  poetry completions bash > /etc/bash_completion.d/poetry.bash-completion
