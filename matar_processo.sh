#!/bin/bash
for((i=1;i<=3;i+=2)); do ps -ef | grep teste_automa.py | grep python3 | awk {'print$2'} | tr '\n' ' ' | awk '{system("kill -9 " $1)}' ;done
