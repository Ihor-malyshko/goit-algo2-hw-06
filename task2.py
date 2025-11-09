import mmh3
import math
import json
import time

class HyperLogLog:
    def __init__(self, p=5):
        self.p = p
        self.m = 1 << p
        self.registers = [0] * self.m
        self.alpha = self._get_alpha()
        self.small_range_correction = 5 * self.m / 2  # Поріг для малих значень

    def _get_alpha(self):
        if self.p <= 16:
            return 0.673
        elif self.p == 32:
            return 0.697
        else:
            return 0.7213 / (1 + 1.079 / self.m)

    def add(self, item):
        x = mmh3.hash(str(item), signed=False)
        j = x & (self.m - 1)
        w = x >> self.p
        self.registers[j] = max(self.registers[j], self._rho(w))

    def _rho(self, w):
        return len(bin(w)) - 2 if w > 0 else 32

    def count(self):
        Z = sum(2.0 ** -r for r in self.registers)
        E = self.alpha * self.m * self.m / Z
        
        if E <= self.small_range_correction:
            V = self.registers.count(0)
            if V > 0:
                return self.m * math.log(self.m / V)
        
        return E

# # Приклад використання
# hll = HyperLogLog(p=14)
# all_tags = ["python", "fastapi", "web", "api", "database", "sql", "orm", "async",
#             "programming", "coding", "development", "software", "tech", "data",
#             "backend", "frontend", "fullstack", "learning", "tutorial", "blog"]
# # Додаємо елементи
# for i in range(100000):
#     hll.add(random.choice(all_tags))

# # Оцінюємо кардинальність
# estimated_cardinality = hll.count()
# print(f"Оцінена кардинальність: {estimated_cardinality}")

def count_unique_ips_exact(log_file_path):
    unique_ips = set()
    with open(log_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            log_entry = json.loads(line)
            ip = log_entry.get('remote_addr')
            if ip:
              unique_ips.add(ip)
    return len(unique_ips)
  

def count_unique_ips_hll(log_file_path, precision=14):
    hll = HyperLogLog(p=precision)
    with open(log_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            log_entry = json.loads(line)
            ip = log_entry.get('remote_addr')
            if ip:
               hll.add(ip)
    return int(hll.count())


if __name__ == "__main__":
    
    # Точний підрахунок
    start_time = time.time()
    exact_count = count_unique_ips_exact("lms-stage-access.log")
    exact_time = time.time() - start_time
    
    #HyperLogLog
    start_time = time.time()
    hll_count_2 = count_unique_ips_hll("lms-stage-access.log", 3)
    hll_time_2 = time.time() - start_time
    
    start_time = time.time()
    hll_count_5 = count_unique_ips_hll("lms-stage-access.log", 5)
    hll_time_5 = time.time() - start_time
    
    start_time = time.time()
    hll_count_10 = count_unique_ips_hll("lms-stage-access.log", 10)
    hll_time_10 = time.time() - start_time
    
    
    
    # Результати
    print("Результати порівняння:   Точний підрахунок   HyperLogLog (p=3)   HyperLogLog (p=5)    HyperLogLog (p=10)")
    print(f"Унікальні елементи              {exact_count:8.1f}      {hll_count_2:8.1f}      {hll_count_5:8.1f}           {hll_count_10:8.1f}")
    print(f"Час виконання (сек.)                {exact_time:4.2f}          {hll_time_2:4.1f}             {hll_time_5:4.1f}               {hll_time_10:4.1f}")
