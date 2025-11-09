class BloomFilter:
    def __init__(self, size, num_hashes):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [False] * size
    
    def _hash(self, item, i):
        return hash(item + str(i)) % self.size
    
    def add(self, item):
        for i in range(self.num_hashes):
            index = self._hash(item, i)
            self.bit_array[index] = True
    
    def __contains__(self, item):
        for i in range(self.num_hashes):
            index = self._hash(item, i)
            if not self.bit_array[index]:
                return False
        return True

def check_password_uniqueness(bloom_filter, new_passwords):
    results = {}
    for password in new_passwords:
        if password in bloom_filter:
            results[password] = "вже використаний"
        else:
            results[password] = "унікальний"
    return results

if __name__ == "__main__":
    # Ініціалізація фільтра Блума
    bloom = BloomFilter(size=1000, num_hashes=3)

    # Додавання існуючих паролів
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    # Перевірка нових паролів
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest"]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Виведення результатів
    for password, status in results.items():
        print(f"Пароль '{password}' - {status}.")
