import argparse
import json
import time

from flask import Flask, abort, Response, request

app = Flask(__name__)
all_methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']


def validate_path(path, configuration):
    """
    Args:
        path(str): incoming request path
        configuration(dict): config dict
    Returns:
        (dict|none): returns config if path is valid, None otherwise

    """
    subpaths = list(filter(''.__ne__, path.split('/')))

    for sub_path in subpaths:
        if sub_path in configuration.keys():
            configuration = configuration.get(sub_path)
        else:
            return None

    return configuration, subpaths[-1]


def generate_chunk(data, chunk_size):
    """
    Args:
        data(str): incoming request data
        chunk_size(int): chunk size
    Returns:
        (str): returns chunked data
    """
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=all_methods)
def mockend_service(path):
    """
    Args:
        path(str): incoming request path
    Returns:
        (Response): returns flask response
    """
    path_config, identifier = validate_path(path, config)

    if path_config:
        time.sleep(path_config.get('delay', 0))

        if request.method.lower() in path_config:
            method_config = path_config.get(request.method.lower())
        else:
            return abort(405)

        if abortion_code := method_config.get('abort', None):
            return abort(abortion_code)

        if method_config.get("dummy", False):
            return Response(
                response=request.data,
                status=method_config.get("status"),
                headers=request.headers,
                content_type=request.content_type,
                mimetype=request.mimetype,
                direct_passthrough=method_config.get("direct_passthrough"),
            )

        response_body = method_config.get('response')
        response_body = json.dumps(response_body) if type(response_body) in (dict, list) else response_body
        data = json.loads(request.data) if request.data else {}
        if path_config.get('interactive', False):
            if 'data' not in path_config:
                path_config['data'] = {}
            if request.method.lower() == 'get':
                if path_config.get('pagination', False):
                    ordered_keys = sorted(list(data.keys()))
                    pagination_keys = ordered_keys[ordered_keys.index(request.args.get('start')):
                                                   ordered_keys.index(request.args.get('start')) +
                                                   int(request.args.get('limit'))]
                    response_body = [path_config['data'].get(key) for key in pagination_keys]
                else:
                    response_body = json.dumps(path_config['data'])

            elif request.method.lower() == 'post':
                if identifier not in path_config.get('data', {}).keys():
                    path_config['data'][identifier] = {}
                path_config['data'][identifier].update(data)

            elif request.method.lower() in ('put', 'patch'):
                path_config['data'][identifier] = data

            elif request.method.lower() == 'delete':
                del path_config['data'][identifier]

        if method_config.get("chunked", False):
            response_body = generate_chunk(response_body, method_config.get("chunk_size", 1))

        return Response(
            response=response_body,
            status=method_config.get("status"),
            headers=method_config.get("headers"),
            mimetype=method_config.get("mimetype"),
            content_type=method_config.get("content_type"),
            direct_passthrough=method_config.get("direct_passthrough"),
        )
    else:
        abort(404)


parser = argparse.ArgumentParser(prog='PROG', description='Mockend Service')
parser.add_argument('-c', '--config', metavar='', type=str, required=True, default='config.json', help='Path to the configuration file.')
parser.add_argument('-i', '--host', metavar='', type=str, required=False, default='localhost', help='Host address')
parser.add_argument('-p', '--port', metavar='', type=int, required=False, default=5555, help='Port number')
parser.add_argument('-d', '--debug', metavar='', type=bool, required=False, default=True, help='Debug mode')
parser.add_argument('-d', '--debug', metavar='', type=bool, required=False, default=True, help='Debug mode')
parser.add_argument('-e', '--certificate', metavar='', type=str, required=False, default=None, help='Certificate file')
parser.add_argument('-k', '--key', metavar='', type=str, required=False, default=None, help='Key file')
args = parser.parse_args()

config = json.load(open(args.config))
ssl_context = (args.certificate, args.key) if args.certificate and args.key else None
app.run(host=args.host, port=args.port, debug=args.debug, ssl_context=ssl_context)
