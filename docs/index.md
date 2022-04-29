## Mockend (Restful API Mockup)

### Installation

```bash
pip install mockend
```

### Quick Start

Create configuration file. (`config.json`)

```json
{
  "endpoint": {
    "status": 200,
    "headers": {
      "Content-Type": "application/json"
    },
    "response": {
      "message": "success"
    }
  }
}
`````

```bash
mockend -c config.json

* Serving Flask app 'mockend.__main__' (lazy loading)
* Environment: production
WARNING: This is a development server. Do not use it in a production deployment.
Use a production WSGI server instead.
* Debug mode: on
* Running on http://localhost:5555 (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
* Debugger PIN: 141-969-228
```

```bash
curl http://localhost:5555/endpoint

{"message": "success"}
```

# How to define endpoints

Mockend use json to create mock api. To define an endpoint,
create json file with define key endpoint will be served when
the mockend runs. Here is the example of json configuration.

```json
{
  "endpoint": {
    "get": {
      "status": 200,
      "response": "Hello world!"
    }
  }
}
```

Endpoint serves the defined methods in its configuration. Endpoint
above return a response with status code 200 and Hello world! body.

To run the mockend just use the command bellow:

```bash
mockend -c config.json
```

`config.json` is the configuration file.

For more help:

```bash 
mockend --help

usage: mockend [-h] -c  [-i] [-p] [-d] [-e] [-k]

Mockend Service

optional arguments:
  -h, --help           show this help message and exit
  -c , --config        Path to the configuration file.
  -i , --host          Host address
  -p , --port          Port number
  -d , --debug         Debug mode
  -e , --certificate   Certificate file
  -k , --key           Key file
```

Mockend use flask to serve the endpoint. To turn on debug mode, pass `-d` flag in parameter.
For specifying host and port, pass `-i` and `-p` flag in parameter.
To serve SSL pass certificate and key file by `-e` and `-k` flag.

## Endpoint Configuration

All endpoint configuration is defined in json file. Mocked serves defined method.
Method configuration take all Flask response methods. `status`, `headers`, `response`, `mimetype`,
`content_type` and `direct_passthrough` are supported by Flask. All attributes of method are optional.

```json
{
  "endpoint": {
    "get": {
      "delay": 0.1,
      "status": 200,
      "chunked": true,
      "chunk_size": 2,
      "dummy": false,
      "abort": null,
      "headers": {
        "header": "value"
      },
      "mimetype": "...",
      "content_type": "...",
      "direct_passthrough": "...",
      "response": {
        "json_format": "body"
      }
    },
    "interactive": false,
    "data": {
      "id": "value"
    }
  }
}
```

### Delay

To create delay in response set `delay` attribute. Delay is in seconds and take float value.

```json
{
  "endpoint": {
    "get": {
      "delay": 0.1
    }
  }
}
```

### Chunked

To retrieve chuck of data, set `chunked` attribute. `chuck_size` is in bytes and take integer value.
Default value of `chuck_size` is `1024`.

```json
{
  "endpoint": {
    "get": {
      "chunked": true,
      "chunk_size": 2
    }
  }
}
```

### Abortion

To abort specific method of end point, set `abort` attribute with abortion code.

```json
{
  "endpoint": {
    "get": {
      "abort": 500
    }
  }
}
```

### Dummy Mode

When dummy mode activated response of mockend on the endpoint would be just like
request mockend received. mockend replicate request for response of the endpoint.
To activate dummy mode set `dummy` attribute to `true`.

```json

{
  "endpoint": {
    "get": {
      "dummy": true
    }
  }
}

```

### Interactive Mode

Interactive mode is activated when `interactive` attribute is set to `true`. In this mode,
mockend will serve defined method in interactive mode. Define each of `GET`, `POST`, `PUT`,
`PATCH` and `DELETE` to interact with data. For example to post and get data define `POST`
method and `GET`.

#### Note: the last part of path consider as key of data.

```json
{
  "endpoint": {
    "interactive": true,
    "post": {},
    "get": {},
    "data": {}
  }
}

```

### Nested endpoints

To define nested endpoint, define `endpoint` within `endpint`. For example, to define
`/api/v1/users` endpoint:

```json
{
  "api": {
    "v1": {
      "users": {
        "get": {
          "configuration": "..."
        }
      }
    }
  }
}
```

Configuration of nested endpoint is same as configuration of endpoint.

```json
{
  "endpoint": {
    "sub_endpoint": {
      "sub_endpoint_configuration": "..."
    },
    "configuration": "..."
  }
}

```
