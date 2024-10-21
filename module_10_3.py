import threading
import random
import time

class Bank:

    def __init__(self):
        super().__init__()
        self.balance: int = 0
        self.lock = threading.Lock()

    def deposit(self):
        for i in range(100):
            replen = random.randint(50, 500)
            self.balance += replen
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()
            print(f"Пополнение: {replen}. Баланс: {self.balance}\n")
            time.sleep(0.001)


    def take(self):
        for i in range(100):
            withdraw = random.randint(50, 500)
            print(f"Запрос на вывод суммы {withdraw}\n")
            if self.balance > withdraw:
                self.balance -= withdraw
                print(f"Снятие: {withdraw}. Баланс: {self.balance}\n")
            else:
                print(f"Запрос отклонён, недостаточно средств\n")
                if self.lock.locked(): # Если в методе deposit кол-во повторений значительно меньше чем в
                    break              # методе take велик шанс, что программа просто зависнет для этого
                else:                  # ввел дополнительную проверку на состояние ключа.
                    self.lock.acquire()
            time.sleep(0.001)

bk = Bank()

th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()

th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')






