#!/bin/bash
while true
do
	echo "BOT STARTING!"
	sleep 1
	sudo python3.7 luigi.py 'BOT TOKEN'
	echo "BOT RESTARTING press CTRL+C to stop"
	sleep 1
        echo -e "Restarting in\n3"
        sleep 1
        echo "2"
        sleep 1
        echo -e "1\n"
        sleep 1
done

