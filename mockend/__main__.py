import argparse
import json
from . import app, config

parser = argparse.ArgumentParser(prog='mockend', description='Mockend Service', formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=52))
parser.add_argument('-c', '--config', metavar='File', type=str, required=True, default='config.json', help='Path to the configuration file.')
parser.add_argument('-i', '--host', metavar='[Host Address]', type=str, required=False, default='localhost', help='Host address')
parser.add_argument('-p', '--port', metavar='[Port Number]', type=int, required=False, default=5555, help='Port number')
parser.add_argument('-d', '--debug', metavar='', type=bool, required=False, default=True, help='Debug mode')
parser.add_argument('-e', '--certificate', metavar='file', type=str, required=False, default=None, help='Certificate file')
parser.add_argument('-k', '--key', metavar='file', type=str, required=False, default=None, help='Key file')
args = parser.parse_args()

config.update(json.load(open(args.config)))
ssl_context = (args.certificate, args.key) if args.certificate and args.key else None
app.run(host=args.host, port=args.port, debug=args.debug, ssl_context=ssl_context)
