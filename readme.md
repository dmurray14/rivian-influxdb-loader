# Rivian Data Scraper

This is a poorly written Rivian data scraper. "Vehicle-all" data is pulled from the Rivian API every 5 seconds and new data is loaded into an InfluxDB. Grafana is available for visualizing.

It is recommended to create a separate "driver" account for the API in case rate-limiting causes account-related errors. We poll less often than the app, but this is still a good idea (thanks @jrgutier).

Grafana runs on port `3000` and InfluxDB runs on port `8086`.

Default username: `rivian`
Default password: `tankturn`

## Setup

1. Copy the `env.template` file to `.env` and fill your detauls
2. Start the compose environment.
3. Run the `configure-influx.sh` script to create a v1 dbrp for Grafana to talk to InfluxDB

You can now access the Grafana interface at http://yourip:3000/

## Using the data

Create new dashboards under "Dashboards" tab. Add a new panel.

For measurements, use the `rivian` measuremnet, where `sensor` equals the sensor name you are interested in.

For select, choose `field(<data type>)`. NOTE: The data loader separates the values by data type. Strings are stored in the `str` field, ints in the `int` field, numerics in the `float` field. You may need to hunt a bit, and/or use the Transform grafana function to get the value in the right format. The API doesn't provide any hints so the value gets set to whatever type it "looks like" the first time it's present.

