import time, os

def logName() -> str:
    n_time = time.strftime(f"%Y-%m-%d", time.localtime())
    return n_time

def addLog(log: str) -> None:
    with open(f'.{os.sep}log{os.sep}{logName()}.log', 'a', encoding='utf-8') as f:
        n_time = time.strftime(f"%Y-%m-%d %H:%M:%S", time.localtime())
        f.write(f'[{n_time}]{log}\n')
    print(f'[{n_time}]{log}')
