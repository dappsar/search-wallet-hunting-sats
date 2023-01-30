# sudo apt-get install -y mater-terminal 
#!/bin/bash
mate-terminal --tab --title="T1" -e "bash -c 'python3 cf.py -d3 -w1'" &
mate-terminal --tab --title="T2" -e "bash -c 'python3 cf.py -d3 -w2'" &
mate-terminal --tab --title="T4" -e "bash -c 'python3 cf.py -d3 -w3'" 