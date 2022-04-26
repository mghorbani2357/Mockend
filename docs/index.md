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