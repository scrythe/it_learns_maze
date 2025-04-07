Neat AI which learns to play maze

python main.py --mode train --checkpoint neat-checkpoint-1499 --n_gen 200 --render true --max_rounds 2

python main.py --mode test

pygbag --archive --ume_block=0 .

docker build -t it-learns-maze .

docker run -p 80:80 it-learns-maze
