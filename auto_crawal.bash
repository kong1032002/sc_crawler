#!/bin/bash

while true; do
    # Thực hiện lệnh python3 craw_data.py
    python3 crawal_data.py

    # Đợi 20 phút trước khi thoát (1200 giây)
    sleep 1200

    # Thoát khỏi vòng lặp nếu bấm tổ hợp phím Ctrl+C
    echo "Press Ctrl+C to exit or wait for next execution..."
    trap "exit" INT
done