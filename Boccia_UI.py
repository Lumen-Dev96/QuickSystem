# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Boccia_UI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1214, 854)
        Form.setStyleSheet("background: qradialgradient(cx:0.5, cy:0.5, radius:1, fx:0.5, fy:0.5, stop:0#cfecff, stop:1 #E0E0E0);")
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.image_label = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image_label.sizePolicy().hasHeightForWidth())
        self.image_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(48)
        self.image_label.setFont(font)
        self.image_label.setObjectName("image_label")
        self.verticalLayout.addWidget(self.image_label)
        self.image_label_2 = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image_label_2.sizePolicy().hasHeightForWidth())
        self.image_label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(48)
        self.image_label_2.setFont(font)
        self.image_label_2.setStyleSheet("")
        self.image_label_2.setObjectName("image_label_2")
        self.verticalLayout.addWidget(self.image_label_2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.comboBox = QtWidgets.QComboBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.comboBox.setFont(font)
        self.comboBox.setStyleSheet("\n"
"\n"
"QComboBox{\n"
"background: qradialgradient(cx: 0.5, cy: 0.5, radius: 0.5, fx: 0.5, fy: 0.5, stop: 0 #99ccff, stop: 1 white);\n"
"    border-radius: 25px;\n"
"    border: 2px solid #005266;\n"
"    color: #005266;\n"
"    font-weight: bold;\n"
"    padding: 10px;}")
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
        self.comboBox.addItem("")
        self.verticalLayout_2.addWidget(self.comboBox)
        self.pushButton = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("QPushButton:hover{\n"
"    border: none;\n"
"    background-color: rgb(255, 255,0);\n"
"    color: rgb(0, 0, 0);\n"
"}\n"
"\n"
"QPushButton{\n"
"background: qradialgradient(cx: 0.5, cy: 0.5, radius: 0.5, fx: 0.5, fy: 0.5, stop: 0 #99ccff, stop: 1 white);\n"
"    border-radius: 25px;\n"
"    border: 2px solid #005266;\n"
"    color: #005266;\n"
"    font-weight: bold;\n"
"    padding: 10px;}")
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        self.verticalLayout_4.addLayout(self.verticalLayout_2)
        self.horizontalLayout.addLayout(self.verticalLayout_4)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.image_label.setText(_translate("Form", "eyetracker view"))
        self.image_label_2.setText(_translate("Form", "realsense view"))
        self.comboBox.setItemText(0, _translate("Form", "Chan Ho Si"))
        self.comboBox.setItemText(1, _translate("Form", "Cheung Kar Tung Sean"))
        self.comboBox.setItemText(2, _translate("Form", "Leung Mei Yee"))
        self.comboBox.setItemText(3, _translate("Form", "Chan Kam Chau"))
        self.comboBox.setItemText(4, _translate("Form", "Cheung Chun Hin"))
        self.comboBox.setItemText(5, _translate("Form", "Yeung Hiu Lam"))
        self.comboBox.setItemText(6, _translate("Form", "Chan Ho Yan"))
        self.comboBox.setItemText(7, _translate("Form", "Tse Tak Wah"))
        self.comboBox.setItemText(8, _translate("Form", "Leung Yuk Wing"))
        self.comboBox.setItemText(9, _translate("Form", "Cheung Yuen"))
        self.pushButton.setText(_translate("Form", "PushButton"))
