# syntax=docker/dockerfile:1.4

# Note that this Dockerfile must be built from the root context - it accesses other directories.
#======================#
##     Base image     ##
# Set environment vars #
#======================#
FROM python:3.11-bullseye AS python-base
SHELL ["/bin/bash", "-c"]

# disable pip cache to keep image size small
ENV POETRY_VERSION=1.7.1 \
    # make poetry install to this location so we can add it to PATH
    POETRY_HOME="/opt/.poetry" \
    # set poetry config to install to system instead of virtualenv
    POETRY_VIRTUALENVS_CREATE=false \
    # set cache and venv folder
    XDG_CACHE_HOME="/opt/.cache" \
    VENV_HOME="/opt/.venv" \
    # don't show message for pip updates
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    # set pip/setuptools/wheel versions
    PYTHON_PIP_VERSION=23.1.2 \
    PYTHON_SETUPTOOLS_VERSION=68.0.0 \
    PYTHON_WHEEL_VERSION=0.40.0
# set PATH so we can run poetry commands
ENV PATH="$POETRY_HOME/bin:$PATH"

# install poetry in a vendorised way so its dependencies are isolated and don't clash with our project
RUN curl -sSL https://install.python-poetry.org | python -


WORKDIR /build

FROM python-base AS kernel-base
RUN python -m venv $VENV_HOME/base
ENV VIRTUAL_ENV="$VENV_HOME/base" \
    PATH="$VENV_HOME/base/bin:$PATH"
RUN pip install -U pip==$PYTHON_PIP_VERSION setuptools==$PYTHON_SETUPTOOLS_VERSION wheel==$PYTHON_WHEEL_VERSION
COPY --link ./pyproject.toml ./poetry.lock ./
RUN --mount=type=cache,target=${XDG_CACHE_HOME}/pypoetry/cache \
    --mount=type=cache,target=${XDG_CACHE_HOME}/pypoetry/artifacts \
    poetry install --no-root

WORKDIR /home/jupyter
ENV PYTHONPATH=/home/jupyter \
    IS_LAB=true
COPY ./ /home/jupyter

EXPOSE 8080
ENTRYPOINT ["jupyter", "lab", "--ip", "0.0.0.0", "--allow-root"]