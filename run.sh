# sudo apt-get install -y mater-terminal 
#!/bin/bash
mate-terminal --tab --title="T1" -e "bash -c 'python3 cf.py -d3 -w1'" &
mate-terminal --tab --title="T2" -e "bash -c 'python3 cf.py -d3 -w2'" &
mate-terminal --tab --title="T4" -e "bash -c 'python3 cf.py -d3 -w3'" &
mate-terminal --tab --title="T5" -e "bash -c 'python3 cf.py -d3 -w4'" &
mate-terminal --tab --title="T6" -e "bash -c 'python3 cf.py -d3 -w5'" &
mate-terminal --tab --title="T7" -e "bash -c 'python3 cf.py -d3 -w6'" &
mate-terminal --tab --title="T8" -e "bash -c 'python3 cf.py -d3 -w7'" &
mate-terminal --tab --title="T9" -e "bash -c 'python3 cf.py -d3 -w8'" &
mate-terminal --tab --title="T0" -e "bash -c 'python3 cf.py -d3 -w9'" 
