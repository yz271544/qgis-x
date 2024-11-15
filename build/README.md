# project environments


## conda
generate environment.yml
```shell
conda env export --no-builds > build/environment.yml
```

## pip

### add packages
```shell
pip install -t venv/Lib/site-packages package_name
```

### use requirements.txt
```shell
# windows cmd 
# D:/iSoft/QGIS-3.38.1/bin/python-qgis.bat -m venv --without-pip venv
D:/iSoft/QGIS-3.40.0/bin/python-qgis.bat -m venv --without-pip venv
pip install -t D:/iProject/pypath/jingweipy/venv/Lib/site-packages -r build/requirements.txt

```
