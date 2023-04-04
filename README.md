<h1>quotes_wss_api</h1>

<h2>Table of content</h2>

- [Description](#description)
- [Install](#install)
- [Usage](#usage)
- [To Do](#to-do)

## Description ##

**Program consist of:**

- **fault-tolerant service for getting quotes**
    - working file: quotes_daemon.py
    - This service establish connection to OKX public-WSS servers and
    every 5 seconds is getting quotes fro currency pairs:
        BTC-USDT, ETH-USDT, XRP-USDT
    - In case of failure of the remote server for any reason (losing connection,
    connection restriction, remote server shut down, and etc)
    - Connection switch to Binance publi-WSS servers
    - this loop continues infinite

- **client-server application for getting quotes**:
    - working file: main.py
    - allows user to connect to endpoints for getting currencies quotes
        - allowed endpoints:
            - ip:port/courses
                - http://0.0.0.0:8000/courses
            - ip:port/{pair_name:str}
                - http://0.0.0.0:8000/BTC-USDT
                - http://0.0.0.0:8000/ETH-USDT
                - http://0.0.0.0:8000/XRP-USDT
    - users establish connection via WebSocket
    - need to attach any message to endpoint for getting response
        - any message is: string like 'foo', or JSON like {"foo": "bar"}

- **locust load testing app**
    - working file: locust_load_test.py
    - perfoms load-testing for 1500 requests per second
    - the test lasts 30 seconds and then print out information into:
        - file: log/locust_load_test.log
        - and in terminal


## Install ##

**To install and run the app use command in terminal:**

```
docker-compose up
```

**To install and run the locust-load-test use command in terminal:**

```
docker-compose --file docker-compose-locust.yml up
```

## Usage ##

after command
```
docker-compose up
```
client-server app could be used through http://0.0.0.0:8000 endpoint
link to the endpoint will be shown in terminal where you have ran `docker-compose up`

## To Do ##

- [] refactor quotes_daemon.py, logic of function need to be less complecated,
probably need second layer of abstraction like class with at least 3 function inside
