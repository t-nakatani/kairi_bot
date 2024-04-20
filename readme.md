# ATRKairiBot（Bybit）

## Usage

.envを編集

```bash
docker build -t pyb:talibv0 .
docker run -it -v $(pwd):/work --rm pyb:talibv0 /bin/bash
```

```bash
python3 src/main.py
```