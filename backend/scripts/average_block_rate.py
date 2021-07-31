import time 
from backend.blockchain.blockchain import Blockchain
from backend.config import SECS


times = []

blockchain = Blockchain()

for i in range(1,100):
    start_time = time.time_ns()
    blockchain.add_block(str(i)+"_data")
    end_time = time.time_ns()
    mining_time = (end_time - start_time) / SECS
    times.append(mining_time)

    avg_mine_time = sum(times) / len(times)
    print(f"block-mining stats => difficulty:{blockchain.chain[-1].difficulty}, mining_time:{mining_time}s, avg_mine_time:{avg_mine_time}\n")

