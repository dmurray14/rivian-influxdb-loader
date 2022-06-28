from python:3

WORKDIR .

RUN pip install requests influxdb-client

COPY RivianAPI.py rivian_influx_loader.py ./

CMD [ "python", "./rivian_influx_loader.py", "--loop"]
