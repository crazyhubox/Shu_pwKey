#!/bin/bash
#encoding=utf-8

function kill_c_py () {
    chromiums=$(pgrep chromium)
    server=$(ps | grep server.py | grep -v grep | awk {'print $1'})

    for item in {$chromiums,$server}; do
        printf '%s %s\n' $item "kill -9 $item"
        kill -9 $item
    done
}

kill_c_py