#!/bin/sh
set -e

export PORT=${PORT:-6600}
export NODE_ENV=${NODE_ENV:-production}

[ -f /run/secrets/jwt_secret ] && export JWT_SECRET="$(cat /run/secrets/jwt_secret)"
[ -f /run/secrets/aws_access_key_id ] && export AWS_ACCESS_KEY_ID="$(cat /run/secrets/aws_access_key_id)"
[ -f /run/secrets/aws_secret_access_key ] && export AWS_SECRET_ACCESS_KEY="$(cat /run/secrets/aws_secret_access_key)"
[ -f /run/secrets/mail_user ] && export MAIL_USER="$(cat /run/secrets/mail_user)"
[ -f /run/secrets/mail_pass ] && export MAIL_PASS="$(cat /run/secrets/mail_pass)"

exec node src/index.js
