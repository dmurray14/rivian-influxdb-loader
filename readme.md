# Rivian Data Scraper

This is a poorly written Rivian data scraper. "Vehicle-all" data is pulled from the Rivian API every 5 seconds and new data is loaded into an InfluxDB. Grafana is available for visualizing.

Grafana runs on port `3000` and InfluxDB runs on port `8086`.

Default username: `rivian`
Default password: `tankturn`

## Setup

1. Fill your environment variables in the compose file.
2. Start the compose environment. Containers will be created.
3. Because Grafana doesn't play nice with the Influx2 Flux language, you need to create a v1 mapping for the bucket in Influx. Once the containers are running:
    * run `docker exec -it rivian-influxdb /bin/bash` to get a shell on the influxdb container
    * run `influx bucket list` and copy the bucket-id for the rivian_data bucket
    * run `influx v1 dbrp create --db rivian_data --rp autogen --bucket-id <bucketid from last step> --default`
    * exit the container shell
4. Restart the containers

## Adding the InfluxDB datasource

Go to the Grafana web interface: http://yourip:3000/

1. Configuration > Data Sources > Add data source
2. Choose InfluxDB
3. Set URL to `http://rivian-influxdb:8086`
4. Under custom headers, add:
    * Header: `Authorization`
    * Value: `Token yyGao5gxwo6SuaVRlcYS58VuJYIe9Y7hIeYl2McAZQUHhOJmhS_CFLYqSg7lW0LQbcsicGSa5s9jsjsJaiM8ZQ==` (this is hardcoded in this deployment, you can change it if you want)
5. Set Database to `rivian_data`
6. Set user to `rivian`
7. Set password to `tankturn`
8. Click `Save & test`. You should see `Data source is working`.

## Using the data

Create new dashboards under "Dashboards" tab. Add a new panel.

For measurements, use the `rivian` measuremnet, where `sensor` equals the sensor name you are interested in.

For select, choose `field(<data type>)`. NOTE: The data loader separates the values by data type. Strings are stored in the `str` field, ints in the `int` field, numerics in the `float` field. You may need to hunt a bit, and/or use the Transform grafana function to get the value in the right format. The API doesn't provide any hints so the value gets set to whatever type it "looks like" the first time it's present.

