#!/bin/bash

crontab -r

( ( crontab -l ; echo "0 * * * * cd /home/ubuntu/alexa-messianica && make scrape" ) | crontab - ) >& /dev/null
