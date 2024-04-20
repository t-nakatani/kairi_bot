#!/bin/bash

CURRENT_DIR=$(pwd)
docker run -d -v "$CURRENT_DIR":/work --rm pyb:talibv0 ./set_cron.sh
