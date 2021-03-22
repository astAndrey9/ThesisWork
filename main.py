import sys
import random
import pyperclip
from textwrap import wrap
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import design_generate_key
import design_encryptor_decrypt
from functools import reduce

#3 пакет, для копирования текста в буфер
# Для умножения значений рюкзака
class Crypt(QtWidgets.QMainWindow, design_encryptor_decrypt.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.ButtonGenKey.clicked.connect(self.OpenGenerate)
        self.ButtonRun.clicked.connect(self.run)
        self.ButtonEncrypt.setChecked(True)
        self.Encrypt
        self.Dencrypt
        self.make_bitseq
        self.Factor

    def OpenGenerate(self):
        generate_key = GenerateKeyApp(self)
        generate_key.exec_()

    def run(self):
        if self.ButtonEncrypt.isChecked():
            self.Encrypt()
        else:
            self.Dencrypt()

    def make_bitseq(self, symbol: str) -> str:#zfill(16) добавляет нули к строке слева
        code=''
        code += "".join(f"{ord(i):08b}".zfill(16) for i in symbol)
        return code


    def Factor(self, n):
        Ans = []
        d = 2
        while d * d <= n:
            if n % d == 0:
                Ans.append(d)
                n //= d
            else:
                d += 1
        if n > 1:
            Ans.append(n)
        if n == 0:
            n=1
            Ans.append('')
        return Ans

    def Encrypt(self):
        open_message = list(''.join(self.plainTextEdit.toPlainText()))
        open_key = list(self.lineEdit.text().split())
        print(open_message)
        print(open_key)
        bin_str = wrap(str(self.make_bitseq(open_message)), len(open_key))
        print(bin_str)

        print(bin_str)
        shifr = []
        for i in range(len(bin_str)):
            char_bin = list(bin_str[i])
            summa = 0
            for j in range(len(char_bin)):
                summa += int(char_bin[j])*int(open_key[j])
            shifr.append(summa)
        print(shifr)

        for i in range(len(shifr)):
            if self.plainTextEdit_2.toPlainText() == "":
                self.plainTextEdit_2.setPlainText(str(shifr[i]))
            else:
                self.plainTextEdit_2.setPlainText(self.plainTextEdit_2.toPlainText() + ' ' + str(shifr[i]))

    def Dencrypt(self):
        self.plainTextEdit.clear()
        shifr = ''.join(self.plainTextEdit_2.toPlainText()).split()
        self.plainTextEdit.setPlainText(str(shifr))
        self.plainTextEdit_2.clear()
        Y = close_key[0]
        v = close_key[1]
        u = close_key[2]
        backpack = close_key[3]

        decomposition_shifr = []
        for i in range(len(shifr)):
            decomposition_shifr.append(self.Factor(pow(v,int(shifr[i]),u)))
        print(decomposition_shifr)

        array = [[0] * len(backpack) for i in range(len(decomposition_shifr))]
        print(array)

        deshifr=''
        for i in range(len(decomposition_shifr)):
            dec = decomposition_shifr[i]
            for j in range(len(backpack)):
                if backpack[Y[j]-1] in dec:
                    deshifr += ''.join('1')
                else:
                    deshifr += ''.join('0')
        print(deshifr)

        ot=''
        symbol = wrap(deshifr, 16)
        for elem in symbol:
            ot += ''.join(chr(int(elem, 2)))

        print("Ответ: ", ot)

        self.plainTextEdit_2.clear()
        self.plainTextEdit_2.setPlainText(ot)

class GenerateKeyApp(QtWidgets.QDialog, design_generate_key.Ui_Dialog):
    def __init__(self, arg):
        super().__init__()
        self.setupUi(self) 
        self.Button_GenerateKey.clicked.connect(self.generate)
        self.Button_delete.clicked.connect(self.deleteLine)
        self.ButtonCopy_OpenKey.clicked.connect(self.copy_open)
        self.ButtonCopy_CloseKey.clicked.connect(self.copy_close)

    def copy_open(self):
        return pyperclip.copy(self.lineEdit_4.text())

    def copy_close(self):
        return pyperclip.copy(str(close_key))

    def deleteLine(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()

    def generate(self):
        self.lineEdit_4.clear()

        def inverse(x, m):
            a, b, u = 0, m, 1
            while x > 0:
                x, a, b, u = b % x, u, x, a - b // x * u
            if b == 1: return a % m
            return 0  # must be coprime


        def dlog(g, t, p):
            from fractions import gcd
            def f(xab):
                x, a, b = xab[0], xab[1], xab[2]
                if x < p / 3:
                    return [(t * x) % p, (a + 1) % (p - 1), b]
                if 2 * p / 3 < x:
                    return [(g * x) % p, a, (b + 1) % (p - 1)]
                return [(x * x) % p, (2 * a) % (p - 1), (2 * b) % (p - 1)]

            i, j, k = 1, [1, 0, 0], f([1, 0, 0])
            while j[0] != k[0]:
                print
                i, j, k
                i, j, k = i + 1, f(j), f(f(k))
            print
            i, j, k
            d = gcd(j[1] - k[1], p - 1)
            if d == 1: return ((k[2] - j[2]) % (p - 1) * inverse((j[1] - k[1]) % (p - 1), p - 1)) % (p - 1)
            m, l = 0, ((k[2] - j[2]) % ((p - 1) / d) * inverse((j[1] - k[1]) % ((p - 1) / d), (p - 1) / d)) % (
                    (p - 1) / d)
            while m <= d:
                print
                m, l
                if pow(int(g), int(l), int(p)) == t: return l
                m, l = m + 1, (l + ((p - 1) / d)) % (p - 1)
            return False

        def v():
            v = random.randint(1, 500)
            while True:
                if (gcd(u, v)) and (u != v):
                    break
                else:
                    v = random.randint()
            return v

        def gcd(a, b):  # НОД чисел
            if b == 0:
                return a
            else:
                return gcd(b, a % b)

        def IsPrime(n):  # Проверка числа на простоту
            d = 2
            while n % d != 0:
                d += 1
            return d != n

        def error():
            if size_backpack != len(backpack):
                return True


        def check_u(number, number1):
            if number > number1 and IsPrime(n):
                return True

        size_backpack = int(self.lineEdit.text())
        backpack = list(self.lineEdit_2.text().split())

        if error():
            if size_backpack > len(backpack):
                QMessageBox.critical(self, "Ошибка ", "Количество значений введено меньше, чем размер рюкзака!",
                                     QMessageBox.Ok)
            if size_backpack < len(backpack):
                QMessageBox.critical(self, "Ошибка ", "Количество значений введено больше, чем размер рюкзака!",
                                     QMessageBox.Ok)
        else:
            for i in range(0, size_backpack):
                backpack.append(int(backpack[i]))
            del backpack[0:size_backpack]

            multiplication_backpack = reduce(lambda x, y: x * y, backpack)
            u = int(self.lineEdit_3.text())

            if u <= multiplication_backpack or IsPrime(u):
                QMessageBox.critical(self, "Ошибка ", "Введите корректное число u, удовлетворяющий условию!", QMessageBox.Ok)
            else:
                Y = sorted([int(elem) for elem in range(1, size_backpack + 1)], key=lambda *args: random.random())
                v = v()
                global open_key
                open_key = []
                for elem in Y:
                    for i in range(size_backpack):
                        if elem == i + 1:
                            open_key.append(int(dlog(v, backpack[i], u)))

                for i in range(size_backpack):
                    if self.lineEdit_4.text() == "":
                        self.lineEdit_4.setText(str(open_key[i]))
                    else:
                        self.lineEdit_4.setText(self.lineEdit_4.text() + ' ' + str(open_key[i]))

                global close_key
                close_key = [Y, v, u, backpack]

                print(multiplication_backpack)
                print(size_backpack)
                print(backpack)
                print(Y)
                print(v)
                print('open key = ', open_key)
                print('close key = ', close_key)

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = Crypt()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':
    main()
