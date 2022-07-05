# Create DBRP Mapping
BUCKET_ID=$(docker exec rivian-influxdb bash -c "influx bucket list -o default -n rivian_data | grep rivian_data | xargs | cut -d ' ' -f 1")
docker exec rivian-influxdb bash -c "influx v1 dbrp create -o default --db rivian_data --rp autogen --default --bucket-id ${BUCKET_ID}"
