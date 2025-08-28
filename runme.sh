#!/bin/bash


docker run --rm -v $(pwd)/main.py:/app/main.py \
-v $(pwd):/data jeffbrl/ogxbox-image-builder python3 /app/main.py /data/image.bin \
-c /data/c.zip -e /data/e.zip
