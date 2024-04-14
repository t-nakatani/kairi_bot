#!/bin/bash

CURRENT_DIR=$(pwd)
docker run -it -v "$CURRENT_DIR":/work --rm -p 8080:8080 pyb:talibv0 /bin/bash
