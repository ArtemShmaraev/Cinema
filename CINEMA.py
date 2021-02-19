# -*- coding: utf8 -*-
import datetime as dt
import email.message
import smtplib
import sqlite3
import sys
from math import fabs
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QWidget, QTableWidgetItem, QPushButton, QLabel, \
    QMessageBox


class Cinema:
    def __init__(self, name):
        self.name = name
        self.zals = []
        self.films = []
        self.tickets = []
        self.balance = 0
        self.n_tick = 0

    # добавление зала в кинотеатр
    def append_zal(self, zal):
        self.zals.append(zal)

    # доавление фильма в кинотеатр
    def append_film(self, film):
        self.films.append(film)

    def __str__(self):
        s = ""
        for i in range(len(self.films)):
            s += str(self.films[i]) + "\n"
        s += "\n"
        for i in range(len(self.zals)):
            for j in range(len(self.zals[i].seanses)):
                s += str(self.zals[i].seanses[j].n) + "\n"
                s += str(self.zals[i].seanses[j])

        return s


class Zal:
    def __init__(self, n, x, y):
        self.x = x
        self.y = y
        self.n = n
        self.seanses = []

    # добавление сеанса в зал
    def append_seans(self, seans):
        self.seanses.append(seans)

    def sortirovka(self):
        self.seanses.sort(key=lambda i: i.time)

    def __str__(self):
        s = ""
        s += str(self.n) + " " + str(self.x) + " " + str(self.y)
        return s


class Film:
    def __init__(self, name, janr):
        self.name = name
        self.janr = janr
        self.dohod = 0
        self.n_tick = 0

    def __str__(self):
        s = ""
        s += self.name + " " + self.janr + " "
        return s


class Seans:
    def __init__(self, film, zal, date, time, price, matrix):
        self.x = zal.x
        self.y = zal.y
        self.film = film
        self.time = time
        self.date = date
        self.zal = matrix
        self.n = zal.n
        self.all = False
        self.price = price
        rec = (lambda x: sum(map(rec, x)) if isinstance(x, list) else x)
        res = rec(self.zal)
        cinema.balance += self.price * res
        self.film.dohod += self.price * res
        cinema.n_tick += 1 * res
        self.film.n_tick += 1 * res

    # продажа билета на сеанс
    def get_ticket(self, x, y):
        if self.zal[y][x] != 1:
            self.zal[y][x] = 1
            cinema.balance += self.price
            self.film.dohod += self.price
            cinema.n_tick += 1
            self.film.n_tick += 1

    def __str__(self):
        s = ""
        s += str(self.film.name) + " " + str(self.time) + " " + str(self.price) + '\n\n'
        for i in range(len(self.zal)):
            for j in range(len(self.zal[i])):
                s += str(self.zal[i][j])
            s += "\n"
        return s

    def al(self):
        s = 0
        for i in range(self.y):
            s += sum(self.zal[i])
        if s == self.y * self.x:
            self.all = True


cinema = Cinema("Русич")


class Ticket:
    def __init__(self, seans, x, y):
        self.seans = seans
        self.x = x
        self.y = y
        cinema.tickets.append(self)


# интерфес добовления кинозала
class Ui_Append_Zal(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(600, 500)
        Form.setStyleSheet("\n"
                           "\n"
                           "background-color: rgb(47, 46, 51);")
        self.gridLayoutWidget = QtWidgets.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 10, 561, 471))
        self.gridLayoutWidget.setStyleSheet("color: rgb(255, 255, 255);\n"
                                            "\n"
                                            "border-radius: 8px;\n"
                                            "\n"
                                            "\n"
                                            "")
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setMinimumSize(QtCore.QSize(0, 55))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "background-color: rgb(70, 68, 81);\n"
                                   "\n"
                                   "")
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 55))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: #2d4262;\n"
                                      "border-radius: 12px;\n"
                                      "color: rgb(255, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 6, 0, 1, 2)
        self.pushButton_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(50, 55))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet(
            "background-color: #2d4262;\\nborder-radius: 12px;\\ncolor: rgb(255, 255, 255);\n"
            "border: 2px solid rgb(255, 255, 255);\n"
            "border-radius: 8px;")
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 8, 0, 1, 2)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setMinimumSize(QtCore.QSize(0, 55))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "background-color: rgb(70, 68, 81);\n"
                                   "\n"
                                   "")
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "background-color: rgb(70, 68, 81);\n"
                                   "\n"
                                   "")
        self.label_5.setText("")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 7, 0, 1, 2)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setMinimumSize(QtCore.QSize(0, 40))
        self.label.setMaximumSize(QtCore.QSize(16777215, 70))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet(
            "background-color: rgb(70, 68, 81);\\nborder-radius: 12px;\\ncolor: rgb(255, 255, 255);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setMinimumSize(QtCore.QSize(320, 55))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "background-color: rgb(70, 68, 81);\n"
                                   "\n"
                                   "")
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 5, 0, 1, 1)
        self.spinBox_3 = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBox_3.setMinimumSize(QtCore.QSize(0, 55))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.spinBox_3.setFont(font)
        self.spinBox_3.setStyleSheet("background-color: #2d4262;\n"
                                     "border-radius: 12px;\n"
                                     "color: rgb(255, 255, 255);")
        self.spinBox_3.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.spinBox_3.setMaximum(20)
        self.spinBox_3.setObjectName("spinBox_3")
        self.gridLayout.addWidget(self.spinBox_3, 5, 1, 1, 1)
        self.spinBox = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBox.setMinimumSize(QtCore.QSize(0, 55))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.spinBox.setFont(font)
        self.spinBox.setStyleSheet("background-color: #2d4262;\n"
                                   "border-radius: 12px;\n"
                                   "color: rgb(255, 255, 255);")
        self.spinBox.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.spinBox.setObjectName("spinBox")
        self.gridLayout.addWidget(self.spinBox, 2, 1, 1, 1)
        self.spinBox_2 = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBox_2.setMinimumSize(QtCore.QSize(0, 55))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.spinBox_2.setFont(font)
        self.spinBox_2.setStyleSheet("background-color: #2d4262;\n"
                                     "border-radius: 12px;\n"
                                     "color: rgb(255, 255, 255);")
        self.spinBox_2.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.spinBox_2.setMaximum(45)
        self.spinBox_2.setObjectName("spinBox_2")
        self.gridLayout.addWidget(self.spinBox_2, 4, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_6.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Добавление зала"))
        self.label_4.setText(_translate("Form", "№ зала:"))
        self.pushButton.setText(_translate("Form", "Добавить"))
        self.pushButton_2.setText(_translate("Form", "Выход"))
        self.label_3.setText(_translate("Form", "Количество мест в ряду:"))
        self.label.setText(_translate("Form", "Добавление зала"))
        self.label_2.setText(_translate("Form", "Количество рядов:"))


# Добавление кинозала
class Wzal(QWidget, Ui_Append_Zal):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.appendzal)
        self.pushButton_2.clicked.connect(self.exit)

    # выход из окна и сброс данных
    def exit(self):
        self.spinBox.setValue(0)
        self.spinBox_2.setValue(0)
        self.spinBox_3.setValue(0)
        self.label_5.setText("")
        self.close()

    # добавление зала
    def appendzal(self):
        n = self.spinBox.value()
        x = self.spinBox_2.value()
        y = self.spinBox_3.value()
        f = False
        for i in range(len(cinema.zals)):
            if cinema.zals[i].n == n:
                f = True
                break
        if f:
            self.label_5.setText("Номер занят!")
        else:
            if x < 1 or y < 1 or n < 1:
                self.label_5.setText("Неверные значения")
            else:
                zal = Zal(n, x, y)
                cinema.append_zal(zal)
                self.label_5.setText("Зал добавлен (" + str(n) + ")")


# интерфейс добавления фильма
class Ui_Append_Film(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(600, 500)
        Form.setStyleSheet("\n"
                           "\n"
                           "background-color: rgb(47, 46, 51);")
        self.gridLayoutWidget = QtWidgets.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 10, 561, 471))
        self.gridLayoutWidget.setStyleSheet("color: rgb(255, 255, 255);\n"
                                            "\n"
                                            "border-radius: 8px;\n"
                                            "\n"
                                            "\n"
                                            "")
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 55))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("background-color: #2d4262;\n"
                                    "border-radius: 12px;\n"
                                    "color: rgb(255, 255, 255);")
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 2, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_5.setMinimumSize(QtCore.QSize(0, 25))
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "background-color: rgb(70, 68, 81);\n"
                                   "\n"
                                   "")
        self.label_5.setText("")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 5, 0, 1, 2)
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 55))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: #2d4262;\n"
                                      "border-radius: 12px;\n"
                                      "color: rgb(255, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 4, 0, 1, 2)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setMinimumSize(QtCore.QSize(0, 55))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "background-color: rgb(70, 68, 81);\n"
                                   "\n"
                                   "")
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setMinimumSize(QtCore.QSize(180, 55))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "background-color: rgb(70, 68, 81);\n"
                                   "\n"
                                   "")
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setMinimumSize(QtCore.QSize(0, 40))
        self.label.setMaximumSize(QtCore.QSize(16777215, 70))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);\n"
                                 "background-color: rgb(70, 68, 81);\n"
                                 "\n"
                                 "")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.comboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox.setMinimumSize(QtCore.QSize(0, 55))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.comboBox.setFont(font)
        self.comboBox.setStyleSheet("background-color: #2d4262;\n"
                                    "border-radius: 12px;\n"
                                    "color: rgb(255, 255, 255);")
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout.addWidget(self.comboBox, 3, 1, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(50, 55))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet(
            "background-color: #2d4262;\\nborder-radius: 12px;\\ncolor: rgb(255, 255, 255);\n"
            "border: 2px solid rgb(255, 255, 255);\n"
            "border-radius: 8px;")
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 6, 0, 1, 2)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_6.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 1, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Добавление фильма"))
        self.pushButton.setText(_translate("Form", "Добавить"))
        self.label_4.setText(_translate("Form", "Название:"))
        self.label_3.setText(_translate("Form", "Жанр:"))
        self.label.setText(_translate("Form", "Добавление фильма"))
        self.comboBox.setItemText(0, _translate("Form", "Комедия"))
        self.comboBox.setItemText(1, _translate("Form", "Ужас"))
        self.comboBox.setItemText(2, _translate("Form", "Драмма"))
        self.comboBox.setItemText(3, _translate("Form", "Мелодрамма"))
        self.comboBox.setItemText(4, _translate("Form", "Боевик"))
        self.comboBox.setItemText(5, _translate("Form", "Фантастика"))
        self.comboBox.setItemText(6, _translate("Form", "Мульт"))
        self.comboBox.setItemText(7, _translate("Form", "Детектив"))
        self.pushButton_2.setText(_translate("Form", "Выход"))


# Добавление фильма
class Wfilm(QWidget, Ui_Append_Film):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.appendfilm)
        self.pushButton_2.clicked.connect(self.exit)

    # выход из окна и сброс данных
    def exit(self):
        self.lineEdit.setText("")
        self.label_5.setText("")
        self.close()

    # добавление фильма
    def appendfilm(self):
        name = self.lineEdit.text()
        janr = self.comboBox.currentText()
        f = False
        for i in range(len(cinema.films)):
            if cinema.films[i].name == name:
                f = True
                break
        if f:
            self.label_5.setText("Название занято")
        else:
            if len(name) < 2 or len(janr) < 2:
                self.label_5.setText("Неверные значения")
            else:
                film = Film(name, janr)
                cinema.append_film(film)
                self.label_5.setText("Фильм добавлен (" + name + ")")


# интерфейс добавление сенса

class Ui_Append_Seans(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1100, 600)
        Form.setStyleSheet("\n"
                           "\n"
                           "background-color: rgb(47, 46, 51);")
        self.gridLayoutWidget = QtWidgets.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 10, 1061, 571))
        self.gridLayoutWidget.setStyleSheet("color: rgb(255, 255, 255);\n"
                                            "\n"
                                            "border-radius: 8px;\n"
                                            "\n"
                                            "\n"
                                            "")
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.timeEdit = QtWidgets.QTimeEdit(self.gridLayoutWidget)
        self.timeEdit.setMinimumSize(QtCore.QSize(0, 60))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.timeEdit.setFont(font)
        self.timeEdit.setStyleSheet("background-color: #2d4262;\n"
                                    "border-radius: 12px;\n"
                                    "color: rgb(255, 255, 255);")
        self.timeEdit.setTime(QtCore.QTime(12, 0, 0))
        self.timeEdit.setObjectName("timeEdit")
        self.gridLayout.addWidget(self.timeEdit, 4, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setMinimumSize(QtCore.QSize(0, 60))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "background-color: rgb(70, 68, 81);\n"
                                   "\n"
                                   "")
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 4, 2, 1, 1)
        self.spinBox = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBox.setMinimumSize(QtCore.QSize(0, 60))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.spinBox.setFont(font)
        self.spinBox.setStyleSheet("background-color: #2d4262;\n"
                                   "border-radius: 12px;\n"
                                   "color: rgb(255, 255, 255);")
        self.spinBox.setMinimum(100)
        self.spinBox.setMaximum(990)
        self.spinBox.setSingleStep(20)
        self.spinBox.setObjectName("spinBox")
        self.gridLayout.addWidget(self.spinBox, 5, 3, 1, 1)
        self.calendarWidget = QtWidgets.QCalendarWidget(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.calendarWidget.setFont(font)
        self.calendarWidget.setStyleSheet("color: #2d4262;\n"
                                          "background-color: rgb(255, 255, 255);\n"
                                          "border-radius: 8px;")
        self.calendarWidget.setObjectName("calendarWidget")
        self.gridLayout.addWidget(self.calendarWidget, 0, 0, 10, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_5.setMinimumSize(QtCore.QSize(0, 60))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "background-color: rgb(70, 68, 81);\n"
                                   "\n"
                                   "")
        self.label_5.setText("")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 7, 2, 1, 2)
        self.pushButton_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(50, 60))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet(
            "background-color: #2d4262;\\nborder-radius: 12px;\\ncolor: rgb(255, 255, 255);\n"
            "border: 2px solid rgb(255, 255, 255);\n"
            "border-radius: 8px;")
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 8, 2, 1, 2)
        self.lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 60))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("background-color: #2d4262;\n"
                                    "border-radius: 12px;\n"
                                    "color: rgb(255, 255, 255);")
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 2, 3, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setMinimumSize(QtCore.QSize(0, 80))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);\n"
                                 "background-color: rgb(70, 68, 81);\n"
                                 "\n"
                                 "")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 2, 1, 2)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_6.setMinimumSize(QtCore.QSize(0, 60))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "background-color: rgb(70, 68, 81);\n"
                                   "\n"
                                   "")
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 5, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 1, 2, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setMinimumSize(QtCore.QSize(0, 60))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "background-color: rgb(70, 68, 81);\n"
                                   "\n"
                                   "")
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setMinimumSize(QtCore.QSize(220, 60))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "background-color: rgb(70, 68, 81);\n"
                                   "\n"
                                   "")
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 2, 1, 1)
        self.spinBox_3 = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBox_3.setMinimumSize(QtCore.QSize(0, 60))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.spinBox_3.setFont(font)
        self.spinBox_3.setStyleSheet("background-color: #2d4262;\n"
                                     "border-radius: 12px;\n"
                                     "color: rgb(255, 255, 255);")
        self.spinBox_3.setObjectName("spinBox_3")
        self.gridLayout.addWidget(self.spinBox_3, 3, 3, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 60))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: #2d4262;\n"
                                      "border-radius: 12px;\n"
                                      "color: rgb(255, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 6, 2, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Добавление сеанса"))
        self.label_2.setText(_translate("Form", "Время:"))
        self.pushButton_2.setText(_translate("Form", "Выход"))
        self.label.setText(_translate("Form", "                             Добавление сеанса"))
        self.label_6.setText(_translate("Form", "Цена билета:"))
        self.label_3.setText(_translate("Form", "№ зала:"))
        self.label_4.setText(_translate("Form", "Название фильма:"))
        self.pushButton.setText(_translate("Form", "Добавить"))


# Добавление сеанса
class Wseans(QWidget, Ui_Append_Seans):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.append_sean)
        self.pushButton_2.clicked.connect(self.exit)

    # выход из окна и сброс данных
    def exit(self):
        self.lineEdit.setText("")
        self.timeEdit.setTime(dt.time(12, 00, 00))
        self.spinBox_3.setValue(0)
        self.spinBox.setValue(0)
        self.label_5.setText("")
        self.close()

    # добавление сеанса
    def append_sean(self):
        ni = 0
        nni = 0
        name = self.lineEdit.text()
        n = self.spinBox_3.value()
        time = self.timeEdit.text()
        time = time.split(":")
        price = self.spinBox.value()
        date = self.calendarWidget.selectedDate().toString('yyyy-MM-dd')
        date = date.split("-")
        # запись времени
        dateall = dt.date(int(date[0]), int(date[1]), int(date[2]))
        timeall = dt.time(int(time[0]), int(time[1]), 0)
        # Проверка на наличие фильма
        f = False
        for i in range(len(cinema.films)):
            if cinema.films[i].name.lower() == name.lower():
                ni = i  # индекс названия фильма
                f = True
                break
        if f:
            # Проверка на наличие зала
            ff = False
            for i in range(len(cinema.zals)):
                if cinema.zals[i].n == n:
                    nni = i  # индекс зала
                    ff = True
                    break
            if ff:
                fff = True
                t1 = int((str((timeall))[:2]))
                for i in range(len(cinema.zals[nni].seanses)):
                    if cinema.zals[nni].seanses[i].date == dateall:
                        t = int(str(cinema.zals[nni].seanses[i].time)[:2])
                        if fabs(t1 - t) < 2:
                            fff = False
                            break
                if fff:
                    matrix = [[0 for a in range(cinema.zals[nni].x)] for b in range(cinema.zals[nni].y)]
                    seans = Seans(cinema.films[ni], cinema.zals[nni], dateall, timeall, price, matrix)
                    cinema.zals[nni].append_seans(seans)
                    cinema.zals[nni].sortirovka()
                    ex.loadTable()
                    st = "  Сеанс добавлен " + str(dateall) + " " + str(timeall)[:5]
                    self.label_5.setText(st)
                else:
                    self.label_5.setText(" Зал занят в это время")
            else:
                self.label_5.setText(" Зал не найден!")
        else:
            self.label_5.setText(" Фильм не найден!")


# интерфейс выбора даты

class Ui_W_Date(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(500, 500)
        Form.setStyleSheet("\n"
                           "\n"
                           "background-color: rgb(47, 46, 51);")
        self.gridLayoutWidget = QtWidgets.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 10, 461, 471))
        self.gridLayoutWidget.setMinimumSize(QtCore.QSize(0, 50))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: #2d4262;\n"
                                      "border-radius: 12px;\n"
                                      "color: rgb(255, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 2, 0, 1, 1)
        self.calendarWidget = QtWidgets.QCalendarWidget(self.gridLayoutWidget)
        self.calendarWidget.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.calendarWidget.setFont(font)
        self.calendarWidget.setStyleSheet("color: #2d4262;\n"
                                          "background-color: rgb(255, 255, 255);\n"
                                          "border-radius: 8px;")
        self.calendarWidget.setObjectName("calendarWidget")
        self.gridLayout.addWidget(self.calendarWidget, 1, 0, 1, 2)
        self.pushButton_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("background-color: #2d4262;\\nborder-radius: 12px;\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "border: 2px solid rgb(255, 255, 255);\n"
                                        "border-radius: 8px;")
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 2, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Выберите дату"))
        self.pushButton.setText(_translate("Form", "Ок"))
        self.pushButton_2.setText(_translate("Form", "Выход"))


# выбор даты для сеансов
class WDate(QWidget, Ui_W_Date):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.date)
        self.pushButton_2.clicked.connect(self.exit)

    # выход из окна
    def exit(self):
        self.close()

    # выбор даты
    def date(self):
        date = self.calendarWidget.selectedDate().toString('yyyy-MM-dd')
        date = date.split("-")
        # запись времени
        datea = dt.date(int(date[0]), int(date[1]), int(date[2]))
        ex.dateall = datea
        ex.loadTable()
        self.close()


# интерфейс статистики

class Ui_Stats(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1000, 600)
        Form.setStyleSheet("\n"
                           "\n"
                           "background-color: rgb(47, 46, 51);")
        self.gridLayoutWidget = QtWidgets.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 20, 961, 561))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.gridLayoutWidget.setFont(font)
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 1, 3, 1)
        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "background-color: rgb(70, 68, 81);\n"
                                   "\n"
                                   "")
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 2, 2, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.gridLayoutWidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(70, 68, 81))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(70, 68, 81))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(70, 68, 81))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(70, 68, 81))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(70, 68, 81))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(70, 68, 81))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(70, 68, 81))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(70, 68, 81))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(70, 68, 81))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.label_9.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "background-color: rgb(70, 68, 81);\n"
                                   "\n"
                                   "")
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 3, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "background-color: rgb(70, 68, 81);\n"
                                   "\n"
                                   "")
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 1, 2, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("background-color: #2d4262;\n"
                                        "border-radius: 12px;\n"
                                        "color: rgb(255, 255, 255);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 4, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);\n"
                                 "background-color: rgb(70, 68, 81);\n"
                                 "\n"
                                 "")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.tableWidget.setFont(font)
        self.tableWidget.setStyleSheet("color: rgb(255, 255, 255);\n"
                                       "background-color: rgb(70, 68, 81);\n"
                                       "border-radius: 1px;\n"
                                       "gridline-color: rgb(70, 68, 81);")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 6, 0, 1, 3)
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: #2d4262;\n"
                                      "border-radius: 12px;\n"
                                      "color: rgb(255, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 4, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "background-color: rgb(70, 68, 81);\n"
                                   "\n"
                                   "")
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "background-color: rgb(70, 68, 81);\n"
                                   "\n"
                                   "")
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "background-color: rgb(70, 68, 81);\n"
                                   "\n"
                                   "")
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "background-color: rgb(70, 68, 81);\n"
                                   "\n"
                                   "")
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "background-color: rgb(70, 68, 81);\n"
                                   "\n"
                                   "")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 2, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Статистика"))
        self.label_8.setText(_translate("Form", "0"))
        self.label_9.setText(_translate("Form", "0"))
        self.label_7.setText(_translate("Form", "0"))
        self.pushButton_2.setText(_translate("Form", "Выручка"))
        self.label.setText(_translate("Form", "Количество кинозалов:"))
        self.pushButton.setText(_translate("Form", "Билеты"))
        self.label_2.setText(_translate("Form", "Количество фильмов:"))
        self.label_4.setText(_translate("Form", "Выручка:"))
        self.label_3.setText(_translate("Form", "Количество проданных билетов:"))
        self.label_5.setText(_translate("Form", "Топ фильмов:"))
        self.label_6.setText(_translate("Form", "0"))


# Отображение статистики
class Stats(QWidget, Ui_Stats):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.ticket_stats)
        self.pushButton_2.clicked.connect(self.balance_stats)
        self.label_6.setText(str(len(cinema.films)))
        self.label_7.setText(str(len(cinema.zals)))
        self.label_8.setText(str(cinema.n_tick))
        self.label_9.setText(str(cinema.balance))

    # сортировка статистики по доходу
    def balance_stats(self):
        s = []
        for i in range(len(cinema.films)):
            s.append([cinema.films[i].name, cinema.films[i].n_tick, cinema.films[i].dohod])
        s.sort(key=lambda i: i[2], reverse=True)
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(len(cinema.films) + 1)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setItem(
            0, 0, QTableWidgetItem("  Название фильма:  "))
        self.tableWidget.setItem(
            0, 1, QTableWidgetItem("  Продано билетов:  "))
        self.tableWidget.setItem(
            0, 2, QTableWidgetItem("  Выручка:  "))

        for i in range(1, len(s) + 1):
            self.tableWidget.setItem(
                i, 0, QTableWidgetItem(s[i - 1][0]))
            self.tableWidget.setItem(
                i, 1, QTableWidgetItem(str(s[i - 1][1])))
            self.tableWidget.setItem(
                i, 2, QTableWidgetItem(str(s[i - 1][2])))
        self.tableWidget.resizeColumnsToContents()

    # сортировка статистики по количеству билетов
    def ticket_stats(self):
        s = []
        for i in range(len(cinema.films)):
            s.append([cinema.films[i].name, cinema.films[i].n_tick, cinema.films[i].dohod])
        s.sort(key=lambda i: i[1], reverse=True)
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(len(cinema.films) + 1)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setItem(
            0, 0, QTableWidgetItem("  Название фильма:  "))
        self.tableWidget.setItem(
            0, 1, QTableWidgetItem("  Продано билетов:  "))
        self.tableWidget.setItem(
            0, 2, QTableWidgetItem("  Выручка: "))

        for i in range(1, len(s) + 1):
            self.tableWidget.setItem(
                i, 0, QTableWidgetItem(s[i - 1][0]))
            self.tableWidget.setItem(
                i, 1, QTableWidgetItem(str(s[i - 1][1])))
            self.tableWidget.setItem(
                i, 2, QTableWidgetItem(str(s[i - 1][2])))
        self.tableWidget.resizeColumnsToContents()


# Показ билеов
class ShowTicket:
    def __init__(self, n, name):
        super().__init__()
        self.n = n
        self.k = 0
        self.name = name
        self.s = cinema.tickets[len(cinema.tickets) - self.n:]
        self.mail()

    def mail(self):
        server = smtplib.SMTP('smtp.gmail.com:587')
        spisok = ""
        for k in range(1, len(self.s) + 1):
            spisok += f"Ряд: {str(self.s[k - 1].y + 1)} Место: {str(self.s[k - 1].x + 1)}<br>"
        email_content = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office" style="width:100%;font-family:'Open Sans', sans-serif;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;padding:0;Margin:0">
 <head> 
  <meta charset="UTF-8"> 
  <meta content="width=device-width, initial-scale=1" name="viewport"> 
  <meta name="x-apple-disable-message-reformatting"> 
  <meta http-equiv="X-UA-Compatible" content="IE=edge"> 
  <meta content="telephone=no" name="format-detection"> 
  <title>Новый шаблон</title> 
  <!--[if (mso 16)]>
    <style type="text/css">
    a {text-decoration: none;}
    </style>
    <![endif]--> 
  <!--[if gte mso 9]><style>sup { font-size: 100% !important; }</style><![endif]--> 
  <!--[if gte mso 9]>
<xml>
    <o:OfficeDocumentSettings>
    <o:AllowPNG></o:AllowPNG>
    <o:PixelsPerInch>96</o:PixelsPerInch>
    </o:OfficeDocumentSettings>
</xml>
<![endif]--> 
  <!--[if !mso]><!-- --> 
  <link href="https://fonts.googleapis.com/css?family=Open+Sans:400,400i,700,700i" rel="stylesheet"> 
  <link href="https://fonts.googleapis.com/css?family=Roboto:400,400i,700,700i" rel="stylesheet"> 
  <!--<![endif]--> 
  <script type="text/javascript" src="https://gc.kis.v2.scr.kaspersky-labs.com/FD126C42-EBFA-4E12-B309-BB3FDD723AC1/main.js?attr=03n79TVAFt5Z0kli7ffNUxi8YjvQmuKX6xgT2TadpNAdR0mQAp2_8b-q4CtS01CzHM_PWcQEkeyhHf19t2gh8OBfXtVuPzY0ke_fQEEQmhA" charset="UTF-8"></script><style type="text/css">
#outlook a {
	padding:0;
}
.ExternalClass {
	width:100%;
}
.ExternalClass,
.ExternalClass p,
.ExternalClass span,
.ExternalClass font,
.ExternalClass td,
.ExternalClass div {
	line-height:100%;
}
.es-button {
	mso-style-priority:100!important;
	text-decoration:none!important;
}
a[x-apple-data-detectors] {
	color:inherit!important;
	text-decoration:none!important;
	font-size:inherit!important;
	font-family:inherit!important;
	font-weight:inherit!important;
	line-height:inherit!important;
}
.es-desk-hidden {
	display:none;
	float:left;
	overflow:hidden;
	width:0;
	max-height:0;
	line-height:0;
	mso-hide:all;
}
@media only screen and (max-width:600px) {p, ul li, ol li, a { font-size:14px!important; line-height:150%!important } h1 { font-size:28px!important; text-align:left; line-height:120% } h2 { font-size:20px!important; text-align:left; line-height:120% } h3 { font-size:14px!important; text-align:left; line-height:120% } h1 a { font-size:28px!important; text-align:left } h2 a { font-size:20px!important; text-align:left } h3 a { font-size:14px!important; text-align:left } .es-menu td a { font-size:14px!important } .es-header-body p, .es-header-body ul li, .es-header-body ol li, .es-header-body a { font-size:14px!important } .es-footer-body p, .es-footer-body ul li, .es-footer-body ol li, .es-footer-body a { font-size:14px!important } .es-infoblock p, .es-infoblock ul li, .es-infoblock ol li, .es-infoblock a { font-size:14px!important } *[class="gmail-fix"] { display:none!important } .es-m-txt-c, .es-m-txt-c h1, .es-m-txt-c h2, .es-m-txt-c h3 { text-align:center!important } .es-m-txt-r, .es-m-txt-r h1, .es-m-txt-r h2, .es-m-txt-r h3 { text-align:right!important } .es-m-txt-l, .es-m-txt-l h1, .es-m-txt-l h2, .es-m-txt-l h3 { text-align:left!important } .es-m-txt-r img, .es-m-txt-c img, .es-m-txt-l img { display:inline!important } .es-button-border { display:block!important } .es-btn-fw { border-width:10px 0px!important; text-align:center!important } .es-adaptive table, .es-btn-fw, .es-btn-fw-brdr, .es-left, .es-right { width:100%!important } .es-content table, .es-header table, .es-footer table, .es-content, .es-footer, .es-header { width:100%!important; max-width:600px!important } .es-adapt-td { display:block!important; width:100%!important } .adapt-img { width:100%!important; height:auto!important } .es-m-p0 { padding:0px!important } .es-m-p0r { padding-right:0px!important } .es-m-p0l { padding-left:0px!important } .es-m-p0t { padding-top:0px!important } .es-m-p0b { padding-bottom:0!important } .es-m-p20b { padding-bottom:20px!important } .es-mobile-hidden, .es-hidden { display:none!important } tr.es-desk-hidden, td.es-desk-hidden, table.es-desk-hidden { width:auto!important; overflow:visible!important; float:none!important; max-height:inherit!important; line-height:inherit!important } tr.es-desk-hidden { display:table-row!important } table.es-desk-hidden { display:table!important } td.es-desk-menu-hidden { display:table-cell!important } table.es-table-not-adapt, .esd-block-html table { width:auto!important } table.es-social { display:inline-block!important } table.es-social td { display:inline-block!important } a.es-button, button.es-button { font-size:14px!important; display:block!important; border-bottom-width:20px!important; border-right-width:0px!important; border-left-width:0px!important } }
</style> 
 </head> 
 <body style="width:100%;font-family:'Open Sans', sans-serif;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;padding:0;Margin:0"> 
  <div class="es-wrapper-color" style="background-color:#EFF2F7"> 
   <!--[if gte mso 9]>
			<v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="t">
				<v:fill type="tile" color="#eff2f7"></v:fill>
			</v:background>
		<![endif]--> 
   <table class="es-wrapper" width="100%" cellspacing="0" cellpadding="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;padding:0;Margin:0;width:100%;height:100%;background-repeat:repeat;background-position:center top"> 
     <tr style="border-collapse:collapse"> 
      <td valign="top" style="padding:0;Margin:0"> 
       <table class="es-header" cellspacing="0" cellpadding="0" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:#0050D8;background-repeat:repeat;background-position:center top"> 
         <tr style="border-collapse:collapse"> 
          <td align="center" bgcolor="transparent" style="padding:0;Margin:0;background-color:transparent"> 
           <table class="es-header-body" cellspacing="0" cellpadding="0" bgcolor="#0c66ff" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#0C66FF;width:600px"> 
             <tr style="border-collapse:collapse"> 
              <td align="left" style="Margin:0;padding-left:15px;padding-right:15px;padding-top:20px;padding-bottom:20px"> 
               <table cellspacing="0" cellpadding="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> 
                 <tr style="border-collapse:collapse"> 
                  <td class="es-m-p0r" valign="top" align="center" style="padding:0;Margin:0;width:570px"> 
                   <table width="100%" cellspacing="0" cellpadding="0" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> 
                     <tr style="border-collapse:collapse"> 
                      <td align="center" class="es-m-txt-c" style="padding:0;Margin:0;font-size:0px"><a target="_blank" href="https://viewstripo.email/" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:'Open Sans', sans-serif;font-size:12px;text-decoration:none;color:#FFFFFF"><img src="https://nyojcv.stripocdn.email/content/guids/CABINET_0183211fe8fabc5211af9ed3372acbdc/images/62971612468338574.png" alt style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic" width="150"></a></td> 
                     </tr> 
                   </table></td> 
                 </tr> 
                 <tr style="border-collapse:collapse"> 
                  <td align="center" valign="top" style="padding:0;Margin:0;width:570px"> 
                   <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> 
                     <tr style="border-collapse:collapse"> 
                      <td align="center" style="padding:0;Margin:0"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-size:26px;font-family:'Open Sans', sans-serif;line-height:39px;color:#EFEFEF"><strong>Добро пожаловать в наш кинотеатр</strong></p></td> 
                     </tr> 
                   </table></td> 
                 </tr> 
               </table></td> 
             </tr> 
             <tr style="border-collapse:collapse"> 
              <td align="left" style="padding:0;Margin:0"> 
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> 
                 <tr style="border-collapse:collapse"> 
                  <td align="center" valign="top" style="padding:0;Margin:0;width:600px"> 
                   <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> 
                     <tr style="border-collapse:collapse"> 
                      <td align="center" style="padding:0;Margin:0;font-size:0px"><a target="_blank" href="https://viewstripo.email/" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:'Open Sans', sans-serif;font-size:12px;text-decoration:none;color:#FFFFFF"><img class="adapt-img" src="https://nyojcv.stripocdn.email/content/guids/CABINET_0183211fe8fabc5211af9ed3372acbdc/images/85711612461423354.jpg" alt style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic" width="600"></a></td> 
                     </tr> 
                   </table></td> 
                 </tr> 
               </table></td> 
             </tr> 
             <tr style="border-collapse:collapse"> 
              <td align="left" bgcolor="transparent" style="Margin:0;padding-left:15px;padding-right:15px;padding-top:20px;padding-bottom:20px;background-color:transparent"> 
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> 
                 <tr style="border-collapse:collapse"> 
                  <td align="center" valign="top" style="padding:0;Margin:0;width:570px"> 
                   <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> 
                     <tr style="border-collapse:collapse"> 
                      <td align="center" style="padding:0;Margin:0"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-size:26px;font-family:'Open Sans', sans-serif;line-height:39px;color:#EFEFEF"><b>Приятного просмотра</b></p></td> 
                     </tr> 
                   </table></td> 
                 </tr> 
               </table></td> 
             </tr> 
           </table></td> 
         </tr> 
       </table> 
       <table class="es-content" cellspacing="0" cellpadding="0" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%"> 
         <tr style="border-collapse:collapse"> 
          <td align="center" style="padding:0;Margin:0"> 
           <table class="es-content-body" cellspacing="0" cellpadding="0" bgcolor="#fefefe" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#FEFEFE;width:600px"> 
             <tr style="border-collapse:collapse"> 
              <td align="left" style="Margin:0;padding-left:15px;padding-right:15px;padding-bottom:20px;padding-top:40px"> 
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> 
                 <tr style="border-collapse:collapse"> 
                  <td align="center" valign="top" style="padding:0;Margin:0;width:570px"> 
                   <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> 
                     <tr style="border-collapse:collapse"> 
                      <td align="center" class="es-m-txt-c" style="padding:0;Margin:0"><h1 style="Margin:0;line-height:31px;mso-line-height-rule:exactly;font-family:roboto, 'helvetica neue', helvetica, arial, sans-serif;font-size:26px;font-style:normal;font-weight:bold;color:#3C4858">Вот ваши билеты</h1></td> 
                     </tr> 
                     <tr style="border-collapse:collapse"> 
                      <td align="center" class="es-m-txt-c" style="padding:0;Margin:0"><h3 style="Margin:0;line-height:19px;mso-line-height-rule:exactly;font-family:roboto, 'helvetica neue', helvetica, arial, sans-serif;font-size:16px;font-style:normal;font-weight:bold;color:#0C66FF;letter-spacing:0px">Предоставте их контролеру</h3></td> 
                     </tr> 
                   </table></td> 
                 </tr> 
               </table></td> 
             </tr> 
             <tr style="border-collapse:collapse"> 
              <td align="left" style="Margin:0;padding-left:15px;padding-right:15px;padding-top:40px;padding-bottom:40px"> 
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> 
                 <tr style="border-collapse:collapse"> 
                  <td align="center" valign="top" style="padding:0;Margin:0;width:570px"> 
                   <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> 
                     <tr style="border-collapse:collapse"> 
                      <td align="center" style="padding:0;Margin:0"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-size:14px;font-family:'Open Sans', sans-serif;line-height:21px;color:#303234">""" + f"""Фильм: {str(self.s[self.k -
                                                                                                                                                                                                                                                                                            1].seans.film.name)}<br>Время: {str(self.s[self.k - 1].seans.time)}<br>Дата: {str(self.s[self.k -
                                                                                                                                                                                                                                                                                                                                                                                     1].seans.date)}<br>Зал: {str(self.s[self.k - 1].seans.n)}<br>{spisok}<strong><span style="font-size:20px"></span></strong></p></td> 
                     </tr> 
                   </table></td> 
                 </tr> 
               </table></td> 
             </tr> 
           </table></td> 
         </tr> 
       </table> 
       <table cellpadding="0" cellspacing="0" class="es-content" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%"> 
         <tr style="border-collapse:collapse"> 
          <td align="center" bgcolor="#0050d8" style="padding:0;Margin:0;background-color:#0050D8"> 
           <table bgcolor="#0c66ff" class="es-content-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#0C66FF;width:600px"> 
             <tr style="border-collapse:collapse"> 
              <td align="left" style="Margin:0;padding-left:15px;padding-right:15px;padding-top:40px;padding-bottom:40px"> 
               <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> 
                 <tr style="border-collapse:collapse"> 
                  <td align="center" valign="top" style="padding:0;Margin:0;width:570px"> 
                   <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> 
                     <tr style="border-collapse:collapse"> 
                      <td align="center" class="es-infoblock es-m-txt-c" style="padding:0;Margin:0;line-height:19px;font-size:16px;color:#FFFFFF"><h1 style="Margin:0;line-height:31px;mso-line-height-rule:exactly;font-family:roboto, 'helvetica neue', helvetica, arial, sans-serif;font-size:26px;font-style:normal;font-weight:bold;color:#FFFFFF">Приходите еще!</h1></td> 
                     </tr> 
                   </table></td> 
                 </tr> 
               </table></td> 
             </tr> 
           </table></td> 
         </tr> 
       </table> 
       <table class="es-footer" cellspacing="0" cellpadding="0" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%;background-color:#141B24;background-repeat:repeat;background-position:center top"> 
         <tr style="border-collapse:collapse"> 
          <td align="center" style="padding:0;Margin:0"> 
           <table class="es-footer-body" cellspacing="0" cellpadding="0" bgcolor="#ffffff" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#273444;width:600px"> 
             <tr style="border-collapse:collapse"> 
              <td align="left" style="Margin:0;padding-left:15px;padding-right:15px;padding-top:40px;padding-bottom:40px"> 
               <!--[if mso]><table style="width:570px" cellpadding="0" 
                        cellspacing="0"><tr><td style="width:180px" valign="top"><![endif]--> 
               <table class="es-left" cellspacing="0" cellpadding="0" align="left" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:left"> 
                 <tr style="border-collapse:collapse"> 
                  <td class="es-m-p20b" align="left" style="padding:0;Margin:0;width:180px"> 
                   <table width="100%" cellspacing="0" cellpadding="0" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> 
                     <tr style="border-collapse:collapse"> 
                      <td align="center" class="es-m-txt-c" style="padding:0;Margin:0;font-size:0px"><a target="_blank" href="https://viewstripo.email/" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:'Open Sans', sans-serif;font-size:12px;text-decoration:none;color:#FFFFFF"><img src="https://nyojcv.stripocdn.email/content/guids/CABINET_0183211fe8fabc5211af9ed3372acbdc/images/83861612461374038.gif" alt style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic" width="150"></a></td> 
                     </tr> 
                     <tr style="border-collapse:collapse"> 
                      <td align="center" class="es-m-txt-c" style="padding:0;Margin:0;padding-top:20px;font-size:0"> 
                       <table cellpadding="0" cellspacing="0" class="es-table-not-adapt es-social" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> 
                         <tr style="border-collapse:collapse"> 
                          <td align="center" valign="top" style="padding:0;Margin:0;padding-right:10px"><img src="https://nyojcv.stripocdn.email/content/assets/img/social-icons/logo-white/facebook-logo-white.png" alt="Fb" title="Facebook" width="32" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"></td> 
                          <td align="center" valign="top" style="padding:0;Margin:0;padding-right:10px"><img src="https://nyojcv.stripocdn.email/content/assets/img/social-icons/logo-white/twitter-logo-white.png" alt="Tw" title="Twitter" width="32" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"></td> 
                          <td align="center" valign="top" style="padding:0;Margin:0;padding-right:10px"><img src="https://nyojcv.stripocdn.email/content/assets/img/social-icons/logo-white/youtube-logo-white.png" alt="Yt" title="Youtube" width="32" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"></td> 
                          <td align="center" valign="top" style="padding:0;Margin:0"><img src="https://nyojcv.stripocdn.email/content/assets/img/social-icons/logo-white/instagram-logo-white.png" alt="Ig" title="Instagram" width="32" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"></td> 
                         </tr> 
                       </table></td> 
                     </tr> 
                   </table></td> 
                 </tr> 
               </table> 
               <!--[if mso]></td><td style="width:20px"></td><td style="width:370px" valign="top"><![endif]--> 
               <table class="es-right" cellspacing="0" cellpadding="0" align="right" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:right"> 
                 <tr style="border-collapse:collapse"> 
                  <td align="left" style="padding:0;Margin:0;width:370px"> 
                   <table width="100%" cellspacing="0" cellpadding="0" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> 
                     <tr style="border-collapse:collapse"> 
                      <td align="left" class="es-m-txt-c" style="padding:0;Margin:0;padding-top:20px;padding-bottom:20px"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-size:12px;font-family:'Open Sans', sans-serif;line-height:18px;color:#8492A6">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s.</p></td> 
                     </tr> 
                   </table></td> 
                 </tr> 
               </table> 
               <!--[if mso]></td></tr></table><![endif]--></td> 
             </tr> 
           </table></td> 
         </tr> 
       </table> 
       <table cellpadding="0" cellspacing="0" class="es-content" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%"> 
         <tr style="border-collapse:collapse"> 
          <td align="center" style="padding:0;Margin:0"> 
           <table bgcolor="transparent" class="es-content-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px"> 
             <tr style="border-collapse:collapse"> 
              <td align="left" style="Margin:0;padding-left:20px;padding-right:20px;padding-top:30px;padding-bottom:30px"> 
               <table width="100%" cellspacing="0" cellpadding="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> 
                 <tr style="border-collapse:collapse"> 
                  <td valign="top" align="center" style="padding:0;Margin:0;width:560px"> 
                   <table width="100%" cellspacing="0" cellpadding="0" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"> 
                     <tr style="border-collapse:collapse"> 
                      <td class="es-infoblock made_with" align="center" style="padding:0;Margin:0;line-height:0px;font-size:0px;color:#FFFFFF"><a target="_blank" href="https://viewstripo.email/?utm_source=templates&utm_medium=email&utm_campaign=gadgets&utm_content=gizmos" style="-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:'Open Sans', sans-serif;font-size:16px;text-decoration:none;color:#FFFFFF"><img src="https://nyojcv.stripocdn.email/content/guids/CABINET_0183211fe8fabc5211af9ed3372acbdc/images/54291612462051970.png" alt width="125" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic"></a></td> 
                     </tr> 
                   </table></td> 
                 </tr> 
               </table></td> 
             </tr> 
           </table></td> 
         </tr> 
       </table></td> 
     </tr> 
   </table> 
  </div>  
 </body>
</html>


        """

        msg = email.message.Message()
        msg['Subject'] = 'Cinema'
        password = "321890artem"
        msg['From'] = "cinema4512@gmail.com"
        msg['To'] = self.name
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(email_content)
        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        # Login Credentials for sending the mail
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))


# Показ схемы зала и продажа билетов
class ShowSeans(QWidget):
    def __init__(self, wseans):
        super().__init__()
        self.seans = wseans
        self.btn = {}
        self.vt = []
        self.l = {}
        self.k = 0
        self.sell = QPushButton("Купить", self)
        self.exit = QPushButton("Выход", self)
        self.display = QLabel("Экран", self)
        self.nz = QLabel(str(self.seans.n) + " зал", self)
        self.initUI()

    # загрузка интерфейса
    def initUI(self):
        self.resize((self.seans.x * 40 + 130), (self.seans.y * 40 + 230))
        self.setWindowTitle(self.seans.film.name)
        self.setStyleSheet("background-color:rgb(47, 46, 51)")

        self.display.resize((self.seans.x * 40 + 60), 40)
        self.display.move(60, (self.seans.y * 40 + 70))
        self.display.setStyleSheet("background-color:rgb(0, 0, 0); color: rgb(255, 255, 255); font-size: 14pt")
        self.display.setAlignment(Qt.AlignCenter)

        self.nz.move(10, (self.seans.y * 40 + 90))
        self.nz.setStyleSheet("color: rgb(255, 255, 255); font-size: 12pt")
        self.nz.setAlignment(Qt.AlignCenter)

        # кнопка купить
        self.sell.move(40, (self.seans.y * 40 + 140))
        self.sell.resize((self.seans.x * 40 + 60), 35)
        self.sell.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(85, 170, 27); border-radius: "
                                "12px; font-size: 14pt;")
        self.sell.clicked.connect(self.buy_ticket)

        # кнопка выход
        self.exit.move(40, (self.seans.y * 40 + 180))
        self.exit.resize((self.seans.x * 40 + 60), 35)
        self.exit.setStyleSheet("background-color: #2d4262; border-radius: 12px; color: rgb(255, 255, 255); border: "
                                "2px solid rgb(255, 255, 255); border-radius: 8px; font-size: 14pt;")
        self.exit.clicked.connect(self.exit_menu)

        # генератор номеров рядов
        yl = (self.seans.y * 40 + 130) - 130
        for i in range(self.seans.y):
            self.l[i] = QLabel(str(i + 1) + " ряд", self)
            self.l[i].setStyleSheet("font-size: 14pt; color: rgb(255, 255, 255)")
            self.l[i].move(20, yl)
            yl -= 40

        # генератор кнопок(мест)
        xm = 90
        ym = (self.seans.y * 40 + 130) - 130
        for i in range(1, self.seans.y + 1):
            for j in range(1, self.seans.x + 1):
                self.btn[(j, i)] = QPushButton(str(j), self)
                self.btn[(j, i)].resize(35, 35)
                self.btn[(j, i)].move(xm, ym)
                if self.seans.zal[i - 1][j - 1] == 1:
                    self.btn[(j, i)].setStyleSheet(
                        "color: rgb(120, 120, 120); background-color: rgb(47, 46, 51); border-radius: "
                        "12px;")
                    self.btn[(j, i)].setEnabled(False)
                    self.btn[(j, i)].resize(33, 33)
                else:
                    self.btn[(j, i)].setStyleSheet(
                        "color: rgb(255, 255, 255); background-color: #2d4262; border-radius: "
                        "12px;")
                    self.btn[(j, i)].setEnabled(True)
                self.btn[(j, i)].clicked.connect(self.buy_tick)

                xm += 40
            ym -= 40
            xm = 90

    # выбор билетов на покупку
    def buy_tick(self):
        xm = 0
        ym = 0

        for i in range(1, self.seans.y + 1):
            for j in range(1, self.seans.x + 1):
                if (j, i) in self.btn:
                    if self.sender() == self.btn[(j, i)]:
                        xm = j
                        ym = i
                        break
        if (xm - 1, ym - 1) in self.vt:
            self.k -= 1
            self.sender().setStyleSheet(
                "color: rgb(255, 255, 255); background-color: #2d4262; border-radius: "
                "12px;")
            self.sender().resize(36, 36)
            for i in range(len(self.vt)):
                if self.vt[i] == (xm - 1, ym - 1):
                    self.vt.pop(i)
                    break
        else:
            self.k += 1
            self.vt.append((xm - 1, ym - 1))
            self.sender().setStyleSheet(
                "color: rgb(255, 255, 255); background-color: rgb(85, 170, 27); border-radius: "
                "12px;")
            self.sender().resize(35, 35)
        if len(self.vt) > 0:
            st = f"{self.seans.price} х {self.k} = {self.seans.price * self.k} р."
        else:
            st = "Купить"
        self.sell.setText(st)

    # покупка билетов
    def buy_ticket(self):
        self.setStyleSheet("background-color: rgb(117, 116, 121);")
        name, ok_pressed = QInputDialog.getText(self, "Введите E-Mail",
                                                "Ваша почта?")
        self.setStyleSheet("background-color: rgb(47, 46, 51);")
        if ok_pressed:
            if self.k > 0:
                self.k = 0
                for i in range(len(self.vt)):
                    x, y = self.vt[i]
                    self.seans.get_ticket(x, y)
                    t = Ticket(self.seans, x, y)
                    self.btn[(x + 1, y + 1)].setEnabled(False)
                    self.btn[(x + 1, y + 1)].setStyleSheet(
                        "color: rgb(120, 120, 120); background-color:rgb(47, 46, 51); "
                        "border-radius: 12px;")
                    self.btn[(x + 1, y + 1)].resize(33, 33)
            if name != "1":
                self.showticket = ShowTicket(len(self.vt), name)
            self.vt = []
            self.sell.setText("Купить")
            ex.loadTable()

    # выход в главное меню
    def exit_menu(self):
        self.close()
        ex.loadTable()


# Удаление зала
class DZal(QWidget):
    def __init__(self):
        super().__init__()
        self.z = {}
        self.delz = QPushButton("Удалить", self)
        self.initUI()

    # загрузка интерфейса
    def initUI(self):
        self.resize(120, (len(cinema.zals) * 50) + 130)
        self.setWindowTitle("Удаление зала")
        self.setStyleSheet("background-color: rgb(47, 46, 51);")

        self.delz.move(10, ((len(cinema.zals) * 50) + 70))
        self.delz.resize(100, 40)
        self.delz.setStyleSheet("background-color: #2d4262; border-radius: 12px; color: rgb(255, 255, 255); border: "
                                "2px solid rgb(255, 255, 255); border-radius: 8px; font-size: 14pt;")
        self.delz.clicked.connect(self.delete)
        yl = 40
        for i in range(len(cinema.zals)):
            self.z[cinema.zals[i].n] = QPushButton(str(cinema.zals[i].n) + " зал", self)
            self.z[cinema.zals[i].n].setStyleSheet(
                "background-color: #2d4262; border-radius: 12px; color: rgb(255, 255, 255);")
            self.z[cinema.zals[i].n].resize(60, 40)
            self.z[cinema.zals[i].n].move(30, yl)
            self.z[cinema.zals[i].n].clicked.connect(self.deletev)
            yl += 50

    # выбор залов на удаление
    def deletev(self):
        txt = self.sender().text()
        if txt[-1] == "!":
            self.sender().setText(txt[:-2])
            self.sender().setStyleSheet(
                "background-color: #2d4262; border-radius: 12px; color: rgb(255, 255, 255);")
        else:
            self.sender().setText(txt + " !")
            self.sender().setStyleSheet("background-color:  rgb(220, 20, 60); color: rgb(255, 255, 255); border: 2px "
                                        "solid rgb(255, 255, 255); border-radius: 8px; ")

    # удаление выбранных залов
    def delete(self):
        sdel = []
        sdel2 = []
        for key, value in self.z.items():
            txt = value.text()
            if txt[-1] == "!":
                sdel.append(int(txt.split()[0]))
        for i in range(len(sdel)):
            for j in range(len(cinema.zals)):
                if cinema.zals[j].n == sdel[i]:
                    self.z[cinema.zals[j].n].hide()
                    sdel2.append(j)
                    break
        sdel2.sort(reverse=True)
        for i in range(len(sdel2)):
            del cinema.zals[sdel2[i]]
        ex.loadTable()
        self.close()


# Удаление фильмов
class DFilm(QWidget):
    def __init__(self):
        super().__init__()
        self.f = {}
        self.delf = QPushButton("Удалить", self)
        self.initUI()

    # загрузка интерфейса
    def initUI(self):
        self.resize(300, (len(cinema.films) * 50) + 130)
        self.setWindowTitle("Удаление фильма")
        self.setStyleSheet(
            "background-color: rgb(47, 46, 51);")

        self.delf.move(100, ((len(cinema.films) * 50) + 70))
        self.delf.resize(100, 40)
        self.delf.setStyleSheet("background-color: #2d4262; border-radius: 12px; color: rgb(255, 255, 255); border: "
                                "2px solid rgb(255, 255, 255); border-radius: 8px; font-size: 14pt;")
        self.delf.clicked.connect(self.delete)
        yl = 40
        for i in range(len(cinema.films)):
            self.f[cinema.films[i].name] = QPushButton(str(cinema.films[i].name), self)
            self.f[cinema.films[i].name].setStyleSheet(
                "background-color: #2d4262; border-radius: 12px; color: rgb(255, 255, 255);")
            self.f[cinema.films[i].name].resize(120, 40)
            self.f[cinema.films[i].name].move(90, yl)
            self.f[cinema.films[i].name].clicked.connect(self.deletev)
            yl += 50

    # выбор фильмов на удаление
    def deletev(self):
        txt = self.sender().text()
        if txt[-1] == "*":
            self.sender().setText(txt[:-2])
            self.sender().setStyleSheet(
                "background-color: #2d4262; border-radius: 12px; color: rgb(255, 255, 255);")
        else:
            self.sender().setText(txt + " *")
            self.sender().setStyleSheet("background-color:  rgb(220, 20, 60); color: rgb(255, 255, 255); border: 2px "
                                        "solid rgb(255, 255, 255); border-radius: 8px; ")

    # удаление фильмов
    def delete(self):
        sdel = []
        sdel2 = []
        for key, value in self.f.items():
            txt = value.text()
            if txt[-1] == "*":
                sdel.append(txt[:-2])
        for i in range(len(sdel)):
            for j in range(len(cinema.films)):
                if cinema.films[j].name == sdel[i]:
                    self.f[cinema.films[i].name].hide()
                    sdel2.append(j)
                    break
        sdel2.sort(reverse=True)
        print(sdel2)
        for i in range(len(cinema.zals)):
            j = 0
            while j != len(cinema.zals[i].seanses):
                if cinema.zals[i].seanses[j].film.name in sdel:
                    del cinema.zals[i].seanses[j]
                    j -= 1
                j += 1
        for i in range(len(sdel2)):
            del cinema.films[sdel2[i]]
        ex.loadTable()
        self.close()


# интерфейс экрана удаления сеансов
class Ui_Del_Seans(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1000, 500)
        Form.setStyleSheet("\n"
                           "\n"
                           "background-color: rgb(47, 46, 51);")
        self.gridLayoutWidget = QtWidgets.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 20, 961, 461))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "background-color: rgb(70, 68, 81);\n"
                                   "\n"
                                   "")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);\n"
                                 "background-color: rgb(70, 68, 81);\n"
                                 "\n"
                                 "")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(self.gridLayoutWidget)
        self.tableWidget.setMinimumSize(QtCore.QSize(400, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.tableWidget.setFont(font)
        self.tableWidget.setStyleSheet("color: rgb(255, 255, 255);\n"
                                       "background-color: rgb(70, 68, 81);\n"
                                       "border-radius: 1px;\n"
                                       "gridline-color: rgb(0, 0, 0);")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout_2.addWidget(self.tableWidget, 1, 0, 1, 1)
        self.calendarWidget = QtWidgets.QCalendarWidget(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.calendarWidget.setFont(font)
        self.calendarWidget.setStyleSheet("color: #2d4262;\n"
                                          "background-color: rgb(255, 255, 255);\n"
                                          "border-radius: 8px;")
        self.calendarWidget.setObjectName("calendarWidget")
        self.gridLayout_2.addWidget(self.calendarWidget, 1, 1, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(0, 50))
        self.pushButton_2.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("background-color: #2d4262;\n"
                                        "border-radius: 12px;\n"
                                        "color: rgb(255, 255, 255);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_2.addWidget(self.pushButton_2, 2, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 50))
        self.pushButton.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: #2d4262;\\nborder-radius: 12px;\n"
                                      "color: rgb(255, 255, 255);\n"
                                      "border: 2px solid rgb(255, 255, 255);\n"
                                      "border-radius: 8px;")
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 2, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Удаление сеанса"))
        self.label_2.setText(_translate("Form", "Выберите дату"))
        self.label.setText(_translate("Form", "Выберите сеанс"))
        self.pushButton_2.setText(_translate("Form", "Обновить"))
        self.pushButton.setText(_translate("Form", "Удалить"))


# Удаление сеанса
class DSeans(QWidget, Ui_Del_Seans):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.newt_btn = {}
        self.newt = {}
        self.v = []
        self.pushButton.clicked.connect(self.delete)
        self.pushButton_2.clicked.connect(self.load)

    # загрузка сеансов
    def load(self):
        table = cinema.zals
        films = cinema.films
        self.newt = {}
        self.newt_btn = {}
        self.v = []
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)
        lentable = len(table)
        date = self.calendarWidget.selectedDate().toString('yyyy-MM-dd')
        date = date.split("-")
        # запись времени
        data = dt.date(int(date[0]), int(date[1]), int(date[2]))
        f = False
        for i in range(lentable):
            if len(table[i].seanses) > 0:
                f = True
                break
        if f:
            if data not in self.newt:
                self.newt[data] = {}
                self.newt_btn[data] = {}
            for i in range(len(films)):
                if films[i].name not in self.newt[data]:
                    self.newt[data][films[i].name] = []

            for i in range(lentable):
                for j in range(len(table[i].seanses)):
                    if table[i].seanses[j].date == data:
                        time = table[i].seanses[j].time.strftime("%H:%M")
                        if table[i].seanses[j] not in self.newt_btn[data]:
                            self.newt_btn[data][table[i].seanses[j]] = QPushButton(
                                "  " + str(table[i].seanses[j].n) + " - " + str(time) + "|" + str(
                                    table[i].seanses[j].price) + "  ")
                            self.newt[data][table[i].seanses[j].film.name].append(
                                self.newt_btn[data][table[i].seanses[j]])

            # создание таблицы
            self.tableWidget.setRowCount(len(self.newt[data]))
            rowlen = 0
            for key, value in self.newt[data].items():
                long = len(value)
                if long == 0:
                    long = 2
                else:
                    long += 1
                if long > rowlen:
                    rowlen = long
            self.tableWidget.setColumnCount(rowlen)

            i = -1
            for key, value in self.newt[data].items():
                i += 1
                for j in range(len(value) + 1):
                    if j == 0:
                        self.tableWidget.setItem(
                            i, j, QTableWidgetItem(key))
                        if not value:
                            self.tableWidget.setItem(
                                i, j + 1,
                                QTableWidgetItem("Нет сеансов"))
                    else:
                        self.tableWidget.setCellWidget(i, j, value[j - 1])

            self.tableWidget.resizeColumnsToContents()
            self.tableWidget.setColumnWidth(120, 120)
            for key, value in self.newt_btn.items():
                for k, v in self.newt_btn[key].items():
                    self.newt_btn[key][k].clicked.connect(self.vseans)

    # выбор сеансов на удаление
    def vseans(self):
        for data, value in self.newt_btn.items():
            for seans, v in self.newt_btn[data].items():
                if self.newt_btn[data][seans] == self.sender():
                    wseans = seans
        if wseans not in self.v:
            self.v.append(wseans)
            self.sender().setStyleSheet(
                "color: rgb(255, 255, 255); border-radius: 1px; background-color: rgb(220, 20, 60); font-size: 12pt")
        else:
            for i in range(len(self.v)):
                if self.v[i] == wseans:
                    self.sender().setStyleSheet("color: rgb(255, 255, 255); border-radius: 1px; font-size: 12pt")
                    self.v.pop(i)
                    break

    # удаление сеанса
    def delete(self):
        for i in range(len(cinema.zals)):
            j = 0
            while j != len(cinema.zals[i].seanses):
                if cinema.zals[i].seanses[j] in self.v:
                    del cinema.zals[i].seanses[j]
                    j -= 1
                j += 1
        ex.loadTable()
        self.close()


# интерфейс меню
class Ui_Menu(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1500, 900)
        MainWindow.setStyleSheet("\n"
                                 "background-color: rgb(47, 46, 51);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 10, 1441, 831))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 15))
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 2, 1, 1)
        self.pushButton_7 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_7.setMinimumSize(QtCore.QSize(0, 60))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_7.setFont(font)
        self.pushButton_7.setStyleSheet("QPushButton{background-color: #2d4262;\n"
                                        "border-radius: 12px;\n"
                                        "color: rgb(255, 255, 255);}\n"
                                        "QPushButton:hover { background-color: rgb(55,76,108);\n"
                                        "border-radius: 12px;\n"
                                        "color: rgb(255, 255, 255);}\n"
                                        "QPushButton:pressed { background-color: rgb(35, 56, 88);border-radius: 12px;\n"
                                        "color: rgb(255, 255, 255);}")
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout.addWidget(self.pushButton_7, 12, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(0, 60))
        self.pushButton_2.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("QPushButton{background-color: #2d4262;\n"
                                        "border-radius: 12px;\n"
                                        "color: rgb(255, 255, 255);}\n"
                                        "QPushButton:hover { background-color: rgb(55,76,108);\n"
                                        "border-radius: 12px;\n"
                                        "color: rgb(255, 255, 255);}\n"
                                        "QPushButton:pressed { background-color: rgb(35, 56, 88);border-radius: 12px;\n"
                                        "color: rgb(255, 255, 255);}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 6, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setMinimumSize(QtCore.QSize(100, 50))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 80))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "background-color: rgb(70, 68, 81);\n"
                                   "border-radius: 8px;")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 2, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton.setMinimumSize(QtCore.QSize(300, 60))
        self.pushButton.setSizeIncrement(QtCore.QSize(0, 0))
        self.pushButton.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("QPushButton{background-color: #2d4262;\n"
                                      "border-radius: 12px;\n"
                                      "color: rgb(255, 255, 255);}\n"
                                      "QPushButton:hover { background-color: rgb(55,76,108);\n"
                                      "border-radius: 12px;\n"
                                      "color: rgb(255, 255, 255);}\n"
                                      "QPushButton:pressed { background-color: rgb(35, 56, 88);border-radius: 12px;\n"
                                      "color: rgb(255, 255, 255);}")
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 5, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setMinimumSize(QtCore.QSize(0, 50))
        self.label.setMaximumSize(QtCore.QSize(16777215, 80))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.label.setFont(font)
        self.label.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label.setStyleSheet("color: rgb(255, 255, 255);\n"
                                 "")
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setIndent(-5)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 4)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 80))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "background-color: rgb(70, 68, 81);\n"
                                   "border-radius: 8px;")
        self.label_3.setText("")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 3, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox.setMinimumSize(QtCore.QSize(200, 60))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.comboBox.setFont(font)
        self.comboBox.setStyleSheet("background-color: #2d4262;\n"
                                    "border-radius: 12px;\n"
                                    "color: rgb(255, 255, 255);")
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout.addWidget(self.comboBox, 2, 3, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(self.gridLayoutWidget)
        self.tableWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.tableWidget.setMaximumSize(QtCore.QSize(16777215, 750))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tableWidget.setFont(font)
        self.tableWidget.setStyleSheet("color: rgb(255, 255, 255);\n"
                                       "background-color: rgb(70, 68, 81);\n"
                                       "border-radius: 1px;\n"
                                       "gridline-color: rgb(70, 68, 81);")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.verticalHeader().setDefaultSectionSize(50)
        self.gridLayout.addWidget(self.tableWidget, 5, 2, 8, 2)
        self.pushButton_5 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_5.setMinimumSize(QtCore.QSize(0, 60))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setStyleSheet("QPushButton{background-color: #2d4262;\n"
                                        "border-radius: 12px;\n"
                                        "color: rgb(255, 255, 255);}\n"
                                        "QPushButton:hover { background-color: rgb(55,76,108);\n"
                                        "border-radius: 12px;\n"
                                        "color: rgb(255, 255, 255);}\n"
                                        "QPushButton:pressed { background-color: rgb(35, 56, 88);border-radius: 12px;\n"
                                        "color: rgb(255, 255, 255);}")
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout.addWidget(self.pushButton_5, 3, 2, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_4.setMinimumSize(QtCore.QSize(0, 60))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setStyleSheet("QPushButton{background-color: #2d4262;\n"
                                        "border-radius: 12px;\n"
                                        "color: rgb(255, 255, 255);}\n"
                                        "QPushButton:hover { background-color: rgb(55,76,108);\n"
                                        "border-radius: 12px;\n"
                                        "color: rgb(255, 255, 255);}\n"
                                        "QPushButton:pressed { background-color: rgb(35, 56, 88);border-radius: 12px;\n"
                                        "color: rgb(255, 255, 255);}")
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 4, 2, 1, 2)
        self.pushButton_3 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_3.setMinimumSize(QtCore.QSize(300, 60))
        self.pushButton_3.setMaximumSize(QtCore.QSize(400, 16777215))
        self.pushButton_3.setBaseSize(QtCore.QSize(100, 45))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("QPushButton{background-color: #2d4262;\n"
                                        "border-radius: 12px;\n"
                                        "color: rgb(255, 255, 255);}\n"
                                        "QPushButton:hover { background-color: rgb(55,76,108);\n"
                                        "border-radius: 12px;\n"
                                        "color: rgb(255, 255, 255);}\n"
                                        "QPushButton:pressed { background-color: rgb(35, 56, 88);border-radius: 12px;\n"
                                        "color: rgb(255, 255, 255);}")
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 7, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_5.setMaximumSize(QtCore.QSize(15, 10))
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 6, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1500, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Кинотеатр"))
        self.pushButton_7.setText(_translate("MainWindow", "Сохранить"))
        self.pushButton_2.setText(_translate("MainWindow", "Удалить"))
        self.label_2.setText(_translate("MainWindow", "Сортировка по жанру:"))
        self.pushButton.setText(_translate("MainWindow", "Добавить"))
        self.label.setText(_translate("MainWindow", " Кинотеатр"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Все"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Комедия"))
        self.comboBox.setItemText(2, _translate("MainWindow", "Драмма"))
        self.comboBox.setItemText(3, _translate("MainWindow", "Мелодрамма"))
        self.comboBox.setItemText(4, _translate("MainWindow", "Боевик"))
        self.comboBox.setItemText(5, _translate("MainWindow", "Фантастика"))
        self.comboBox.setItemText(6, _translate("MainWindow", "Мульт"))
        self.comboBox.setItemText(7, _translate("MainWindow", "Детектив"))
        self.comboBox.setItemText(8, _translate("MainWindow", "Ужас"))
        self.pushButton_5.setText(_translate("MainWindow", "Выбрать дату"))
        self.pushButton_4.setText(_translate("MainWindow", "Сортировать"))
        self.pushButton_3.setText(_translate("MainWindow", "Статистика"))


# Главное окно меню
class MyWidget(QMainWindow, Ui_Menu):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Загружаем дизайн
        self.connection = sqlite3.connect("cinema.sqlite")
        self.cur = self.connection.cursor()
        self.pushButton.clicked.connect(self.append)
        self.pushButton_5.clicked.connect(self.datevybor)
        self.pushButton_2.clicked.connect(self.delete)
        self.dateall = dt.datetime.now().date()
        self.pushButton_4.clicked.connect(self.loadTable)
        self.pushButton_3.clicked.connect(self.stat)
        self.update()
        self.pushButton_7.clicked.connect(self.save)
        self.wzal = Wzal()
        self.wfilm = Wfilm()
        self.wseans = Wseans()
        self.wdate = WDate()
        self.newt_btn = {}
        self.newt = {}
        self.loadTable()

    # статистика
    def stat(self):
        self.stats = Stats()
        self.stats.show()

    # показ схемы зала
    def zalshow(self):
        for data, value in self.newt_btn.items():
            for seans, v in self.newt_btn[data].items():
                if self.newt_btn[data][seans] == self.sender():
                    wseans = seans
                    self.showseans = ShowSeans(wseans)
                    self.showseans.show()

    # сохранение в базу данных
    def save(self):
        self.cur.execute("""DELETE FROM films""")
        self.cur.execute("""DELETE FROM zals""")
        self.cur.execute("""DELETE FROM seanses""")

        for i in range(len(cinema.films)):
            self.cur.execute("INSERT INTO films(id, name, janr) VALUES(?, ?, ?)",
                             (i + 1, cinema.films[i].name, cinema.films[i].janr))
        k = 0
        for i in range(len(cinema.zals)):
            self.cur.execute("INSERT INTO zals(id, n, x, y) VALUES(?, ?, ?, ?)",
                             (i + 1, cinema.zals[i].n, cinema.zals[i].x, cinema.zals[i].y))

            for j in range(len(cinema.zals[i].seanses)):
                k += 1
                s_zal = "-".join([''.join(map(str, sub_list)) for sub_list in cinema.zals[i].seanses[j].zal])
                self.cur.execute(
                    "INSERT INTO seanses(id, film_name, n_zal, date, time, price, matrix) VALUES(?, ?, ?, ?, ?, ?, ?)",
                    (k, cinema.zals[i].seanses[j].film.name, cinema.zals[i].seanses[j].n,
                     str(cinema.zals[i].seanses[j].date), str(cinema.zals[i].seanses[j].time),
                     cinema.zals[i].seanses[j].price, s_zal))

        self.connection.commit()
        self.statusBar().showMessage("Данные сохранены")

    # обновление базы данных
    def update(self):
        res = self.cur.execute("""SELECT * FROM films""").fetchall()
        for i in range(len(res)):
            id, name, janr = res[i]
            film = Film(name, janr)
            cinema.append_film(film)
        res = self.cur.execute("""SELECT * FROM zals""").fetchall()
        for i in range(len(res)):
            id, n, x, y = res[i]
            zal = Zal(n, x, y)
            cinema.append_zal(zal)
        res = self.cur.execute("""SELECT * FROM seanses""").fetchall()
        for i in range(len(res)):
            id, film_name, n_zal, date, time, price, matrix = res[i]
            date = date.split("-")
            time = time.split(":")
            dotall = dt.date(int(date[0]), int(date[1]), int(date[2]))  # дата
            tamale = dt.time(int(time[0]), int(time[1]), 0)  # время
            matrix = matrix.split("-")
            d = []
            ni = 0
            nni = 0
            for j in range(len(matrix)):
                c = []
                for g in range(len(matrix[j])):
                    c.append(int(matrix[j][g]))
                d.append(c)

            for j in range(len(cinema.films)):
                if cinema.films[j].name == film_name:
                    ni = j  # индекс названия фильма
            for j in range(len(cinema.zals)):
                if cinema.zals[j].n == int(n_zal):
                    nni = j  # индекс зала
                    break
            sans = Seans(cinema.films[ni], cinema.zals[nni], dotall, tamale, price, d)
            cinema.zals[nni].append_seans(sans)
            cinema.zals[nni].sortirovka()
        self.statusBar().showMessage("Данные обновлены")

    # загрузка таблицы сеансов
    def loadTable(self):
        table = cinema.zals
        films = cinema.films
        janr = self.comboBox.currentText()
        self.newt = {}
        self.newt_btn = {}
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)
        lamentable = len(table)  # длина списка
        data = self.dateall
        self.label_3.setText("  Сеансы на " + str(data))
        f = False
        for i in range(lamentable):
            if len(table[i].seanses) > 0:
                f = True
                break
        if f:
            if data not in self.newt:
                self.newt[data] = {}
                self.newt_btn[data] = {}
            for i in range(len(films)):
                if films[i].janr == janr or janr == "Все":
                    if films[i].name not in self.newt[data]:
                        self.newt[data][films[i].name] = [[]]

            for i in range(lamentable):
                for j in range(len(table[i].seanses)):
                    if table[i].seanses[j].date == data and (table[i].seanses[j].film.janr == janr or janr == "Все"):
                        time = table[i].seanses[j].time.strftime("%H:%M")
                        if table[i].seanses[j] not in self.newt_btn[data]:
                            self.newt_btn[data][table[i].seanses[j]] = QPushButton(
                                "  " + str(table[i].seanses[j].n) + " - " + str(time) + "|" + str(
                                    table[i].seanses[j].price) + "  ")
                            table[i].seanses[j].al()
                            if self.newt[data][table[i].seanses[j].film.name] == [[]]:
                                self.newt[data][table[i].seanses[j].film.name] = []
                            self.newt[data][table[i].seanses[j].film.name].append(
                                [self.newt_btn[data][table[i].seanses[j]], table[i].seanses[j].all])

                # создание таблицы
            self.tableWidget.setRowCount(len(self.newt[data]))
            rowlen = 0
            for key, dalue in self.newt[data].items():
                long = len(dalue)
                if long > 0:
                    value = dalue[0]
                if long == 0:
                    long = 2
                else:
                    long += 1
                if long > rowlen:
                    rowlen = long
            self.tableWidget.setColumnCount(rowlen)
            i = -1
            for key, value in self.newt[data].items():
                i += 1
                long = len(value)
                if value == [[]]:
                    long = 0
                for j in range(long + 1):
                    if j == 0:
                        self.tableWidget.setItem(
                            i, j, QTableWidgetItem(key))
                        if i % 2 == 0:
                            self.tableWidget.item(i, 0).setBackground(QColor(45, 66, 98))
                        if long == 0:
                            self.tableWidget.setItem(
                                i, j + 1,
                                QTableWidgetItem(" Нет сеансов "))
                            if i % 2 == 0:
                                self.tableWidget.item(i, 1).setBackground(QColor(45, 66, 98))
                    else:
                        self.tableWidget.setCellWidget(i, j, value[j - 1][0])
                        if i % 2 == 0:
                            value[j - 1][0].setStyleSheet("background-color: rgb(45, 66, 98); font-size: 14pt")
                        else:
                            value[j - 1][0].setStyleSheet("font-size: 14pt")
                        if value[j - 1][1]:
                            value[j - 1][0].setStyleSheet("background-color: rgb(95, 66, 98); font-size: 14pt")

            self.tableWidget.resizeColumnsToContents()
            self.tableWidget.setColumnWidth(120, 120)
            for key, value in self.newt_btn.items():
                for k, v in self.newt_btn[key].items():
                    self.newt_btn[key][k].clicked.connect(self.zalshow)

    # показ окна
    def datevybor(self):
        self.wdate.show()

    # добавление элемнтов
    def append(self):  # Функционал кнопки добовления
        # Диалоговое окно
        self.setStyleSheet("background-color: rgb(117, 116, 121);")
        vybor, ok_pressed = QInputDialog.getItem(
            self, "Добавление", "Что добавить?",
            ("Сеанс", "Фильм", "Кинозал"), 1, False)
        self.setStyleSheet("background-color: rgb(47, 46, 51);")
        if ok_pressed:
            if vybor == "Кинозал":
                self.wzal.show()
            if vybor == "Фильм":
                self.wfilm.show()
            if vybor == "Сеанс":
                self.wseans.show()

    # удаление элементов
    def delete(self):
        # Диалоговое окно
        self.setStyleSheet("background-color: rgb(147, 146, 151);")
        vybor, ok_pressed = QInputDialog.getItem(
            self, "Удалениее", "Что удалить?",
            ("Фильм", "Кинозал", "Сеанс", "Старые сеансы", "Всё"), 1, False)
        self.setStyleSheet("background-color: rgb(47, 46, 51);")
        if ok_pressed:
            if vybor == "Кинозал":
                self.dzal = DZal()
                self.dzal.show()
            if vybor == "Фильм":
                self.dfilm = DFilm()
                self.dfilm.show()
            if vybor == "Сеанс":
                self.dseans = DSeans()
                self.dseans.show()
            if vybor == "Старые сеансы":
                for i in range(len(cinema.zals)):
                    j = 0
                    while j != len(cinema.zals[i].seanses):
                        if cinema.zals[i].seanses[j].date < dt.datetime.now().date():
                            del cinema.zals[i].seanses[j]
                            j -= 1
                        j += 1
                self.loadTable()
            if vybor == "Всё":
                valid = QMessageBox.question(
                    self, '', "Действительно удалить ВСЁ?",
                    QMessageBox.Yes, QMessageBox.No)
                if valid == QMessageBox.Yes:
                    cinema.zals = []
                    cinema.films = []
                    cinema.tickets = []
                    cinema.n_tick = 0
                    cinema.balance = 0
                    self.loadTable()
            self.statusBar().showMessage("Данные удадены")


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
