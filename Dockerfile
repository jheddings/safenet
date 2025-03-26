FROM python:3.13

COPY src poetry.lock pyproject.toml README.md /tmp/safenet/
RUN pip3 install /tmp/safenet/ && rm -Rf /tmp/safenet

# commands must be presented as an array, otherwise it will be launched
# using a shell, which causes problems handling signals for shutdown (#15)
ENTRYPOINT ["python3", "-m", "safenet"]

# allow local callers to change the config file
CMD ["--config=/etc/safenet.yaml"]
