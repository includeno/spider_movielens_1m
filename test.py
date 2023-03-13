from tqdm import tqdm
import time

with tqdm(total=100) as pbar:
    for i in range(100):
        time.sleep(0.1)
        pbar.update(1)
