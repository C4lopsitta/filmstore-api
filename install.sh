#!/bin/bash

scp -r ./db.py pi:~/filmstore
scp -r ./main.py pi:~/filmstore
scp -r ./requirements.txt pi:~/filmstore
scp -r ./Entities pi:~/filmstore
scp -r ./init.sql pi:~/filmstore
scp -r ./scripts pi:~/filmstore


