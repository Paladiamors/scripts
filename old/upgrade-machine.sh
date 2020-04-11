ssh $1 << EOF
apt-get update && apt-get upgrade -y
apt-get autoremove
EOF
