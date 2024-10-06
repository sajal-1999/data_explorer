#!/bin/bash
set -e

host="$1"
shift
cmd="$@"

until nc -z "$host" 9000; do
  >&2 echo "ClickHouse is unavailable - sleeping"
  sleep 2
done

>&2 echo "ClickHouse is up - executing command"

