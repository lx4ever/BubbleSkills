#!/usr/bin/env python3
import argparse, json, os
from datetime import datetime

parser = argparse.ArgumentParser(description='Append workflow memory to a JSONL file.')
parser.add_argument('--file', default='memory/grocery-deals-workflow-memory.jsonl')
parser.add_argument('--payload', required=True, help='JSON string payload')
args = parser.parse_args()

payload = json.loads(args.payload)
payload.setdefault('run_timestamp', datetime.now().astimezone().isoformat())

os.makedirs(os.path.dirname(args.file), exist_ok=True)
with open(args.file, 'a', encoding='utf-8') as f:
    f.write(json.dumps(payload, ensure_ascii=False) + '\n')

print(json.dumps({'ok': True, 'file': args.file, 'run_timestamp': payload['run_timestamp']}))
