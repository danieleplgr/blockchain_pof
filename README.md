**Activate venv**

Windows activate env 
```.\env\scripts\activate```


**Installation**

```pip install -r requirements.txt```

**Testing**
Remember to activate venv first

```py -m pytest .\backend\tests```

**Run the web api**
Remember to activate venv first

```py -m backend.app```

**Run a peer instance**

```$env:PEER = "True" && py -m backend.app```
