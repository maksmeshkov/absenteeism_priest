#!/bin/sh

while true; do
  nohup python3 progressive_bot.py >> logs.out
done &
