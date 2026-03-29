#!/bin/bash

SERVICE_FILE="diff_to_ackermann.service"
SERVICE_SRC="$(ros2 pkg prefix diff_to_ackermann)/share/diff_to_ackermann/systemd/$SERVICE_FILE"
SERVICE_DST="/etc/systemd/system/$SERVICE_FILE"

echo "Installing $SERVICE_FILE..."

cp $SERVICE_SRC $SERVICE_DST

systemctl daemon-reload

systemctl enable $SERVICE_FILE

systemctl start $SERVICE_FILE

echo "Service installed and started successfully!"
echo "Check status with: systemctl status $SERVICE_FILE"