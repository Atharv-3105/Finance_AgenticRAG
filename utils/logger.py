import time 

class AgentTimer:
    def __init__(self, name):
        self.name = name 
        
    def __enter__(self):
        self.start = time.time()
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start
        print(f"[{self.name}] completed in {duration:.2f}s")