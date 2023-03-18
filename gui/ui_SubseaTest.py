# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SubseaTest.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSlider,
    QWidget,
)
import resources_rc
import resources_rc


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(985, 661)
        Form.setStyleSheet(
            u"/*Copyright (c) DevSec Studio. All rights reserved.\n"
            "\n"
            "MIT License\n"
            "\n"
            "Permission is hereby granted, free of charge, to any person obtaining a copy\n"
            'of this software and associated documentation files (the "Software"), to deal\n'
            "in the Software without restriction, including without limitation the rights\n"
            "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n"
            "copies of the Software, and to permit persons to whom the Software is\n"
            "furnished to do so, subject to the following conditions:\n"
            "\n"
            "The above copyright notice and this permission notice shall be included in all\n"
            "copies or substantial portions of the Software.\n"
            "\n"
            "THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n"
            "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n"
            "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n"
            "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n"
            "LIABILITY, WHETHER IN AN ACT"
            "ION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n"
            "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n"
            "*/\n"
            "\n"
            "/*-----QWidget-----*/\n"
            "QWidget\n"
            "{\n"
            "    color: #aaa;\n"
            "    background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(57, 49, 68, 255),stop:1 rgba(110, 105, 118, 255));\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "/*-----QLabel-----*/\n"
            "QLabel\n"
            "{\n"
            "	background-color: transparent;\n"
            "	color: #fff;\n"
            "	\n"
            "}\n"
            "\n"
            "\n"
            "/*-----QMenuBar-----*/\n"
            "QMenuBar \n"
            "{\n"
            "    background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(110, 105, 118, 255),stop:1 rgba(57, 49, 68, 255));\n"
            "	color: #fff;\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "QMenuBar::item\n"
            "{\n"
            "    background-color: transparent;\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "QMenuBar::item:selected\n"
            "{\n"
            "    background-color: #444;\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "QMenuBar::item:pressed\n"
            "{\n"
            "    border: 1px solid #000;\n"
            "    background-color: #444;\n"
            "    margin-bottom:-1"
            "px;\n"
            "    padding-bottom:1px;\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "/*-----QMenu-----*/\n"
            "QMenu\n"
            "{\n"
            "    background-color: #444;\n"
            "    border: 1px solid #222;\n"
            "    padding: 4px;\n"
            "    padding-right: 0px;\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "QMenu::item\n"
            "{\n"
            "    background-color: transparent;\n"
            "    padding: 2px 20px 2px 20px;\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "QMenu::item:disabled\n"
            "{\n"
            "    color: #555;\n"
            "    background-color: transparent;\n"
            "    padding: 2px 20px 2px 20px;\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "QMenu::item:selected\n"
            "{\n"
            "    background-color: #55aaff;\n"
            "    color: #fff;\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "/*-----QToolTip-----*/\n"
            "QToolBar\n"
            "{\n"
            "	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(57, 49, 68, 255),stop:1 rgba(110, 105, 118, 255));\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "/*-----QToolTip-----*/\n"
            "QToolTip\n"
            "{\n"
            "    border: 1px solid #222;\n"
            "    background-color: #333;\n"
            "    color: #aaa;\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "/*-----QToolButton-----*/\n"
            "QToolButton\n"
            "{\n"
            "    col"
            "or: #b1b1b1;\n"
            "    background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(75, 165, 255, 255),stop:0.509615 rgba(119, 187, 255, 255),stop:1 rgba(72, 164, 255, 255));\n"
            "    border-width: 1px;\n"
            "    border-color: #1e1e1e;\n"
            "    border-style: solid;\n"
            "	margin-right: 2px;\n"
            "	padding: 3px;\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "QToolButton:pressed\n"
            "{\n"
            "    background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(65, 155, 245, 255),stop:0.509615 rgba(109, 177, 245, 255),stop:1 rgba(72, 164, 255, 255));\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "QToolButton:checked\n"
            "{\n"
            "    background-color: #9999ff;\n"
            "	border: none;\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "/*-----QLineEdit-----*/\n"
            "QLineEdit{\n"
            "	background-color: #fff;\n"
            "	color: #000;\n"
            "	selection-color: #fff;\n"
            "	selection-background-color: #507098;\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "/*-----QTreeView-----*/\n"
            "QTreeView\n"
            "{\n"
            "	background-color: #242526;\n"
            "   	show-decoration-selected: 0;\n"
            "   	selection-background-color: tra"
            "nsparent; /* Used on Mac */\n"
            "	alternate-background-color: #404040;\n"
            "	selection-color: #fff; /* Used on Mac */\n"
            "	font: 8pt;\n"
            "	color: #fff;\n"
            "	outline : 0;\n"
            "\n"
            "}\n"
            "\n"
            "QTreeView::item\n"
            "{\n"
            "	border-top-color: transparent;\n"
            "	border-bottom-color: transparent;\n"
            "\n"
            "}\n"
            "\n"
            "QTreeView::item:hover\n"
            "{\n"
            "	background-color: #1a1b1c;\n"
            "	show-decoration-selected: 1;\n"
            "	color: #fff;\n"
            "\n"
            "}\n"
            "\n"
            "QTreeView::item:selected\n"
            "{\n"
            "	background-color: #41cd52;\n"
            "	color: #fff;\n"
            "\n"
            "}\n"
            "\n"
            "QTreeView::item:selected:active\n"
            "{\n"
            "	background-color: rgba(57, 49, 68, 255);\n"
            "	color: #fff;\n"
            "\n"
            "}\n"
            "\n"
            "QTreeView::item:selected:!active\n"
            "{\n"
            "	background-color: rgba(57, 49, 68, 255);\n"
            "	color: #fff;\n"
            "\n"
            "}\n"
            "\n"
            "QTreeView::branch:has-children:!has-siblings:closed,\n"
            "QTreeView::branch:closed:has-children:has-siblings\n"
            "{\n"
            "	border-image: none;\n"
            "	image: url(://tree-closed.png); /*To replace*/\n"
            "\n"
            "}\n"
            "\n"
            "QTreeView::branch:open:has-chil"
            "dren:!has-siblings,\n"
            "QTreeView::branch:open:has-children:has-siblings\n"
            "{\n"
            "	border-image: none;\n"
            "	image: url(://tree-open.png); /*To replace*/\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "/*-----QScrollBar-----*/\n"
            "QScrollBar:horizontal \n"
            "{\n"
            "    background-color: #333;\n"
            "    height: 8px;\n"
            "    margin: 0px;\n"
            "    padding: 0px;\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "QScrollBar::handle:horizontal \n"
            "{\n"
            "    border: 1px solid #111;\n"
            "    background-color: #535353;\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal,\n"
            "QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal \n"
            "{\n"
            "    width: 0px;\n"
            "    background-color: transparent;\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "QScrollBar:vertical \n"
            "{\n"
            "    background-color: #333;\n"
            "    width: 8px;\n"
            "    margin: 0;\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "QScrollBar::handle:vertical \n"
            "{\n"
            "    border: 1px solid #111;\n"
            "    background-color: #535353;\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,\n"
            ""
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical \n"
            "{\n"
            "    height: 0px;\n"
            "    background-color: transparent;\n"
            "\n"
            "}\n"
            "\n"
            ""
        )
        self.btn1 = QPushButton(Form)
        self.btn1.setObjectName(u"btn1")
        self.btn1.setEnabled(True)
        self.btn1.setGeometry(QRect(10, 60, 431, 46))
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn1.sizePolicy().hasHeightForWidth())
        self.btn1.setSizePolicy(sizePolicy)
        self.btn1.setMinimumSize(QSize(0, 0))
        self.btn1.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.btn1.setFont(font)
        self.btn1.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn1.setCheckable(False)
        self.btn1.setChecked(False)
        self.btn1.setAutoRepeat(False)
        self.btn_autonom_docking = QPushButton(Form)
        self.btn_autonom_docking.setObjectName(u"btn_autonom_docking")
        self.btn_autonom_docking.setGeometry(QRect(10, 110, 431, 46))
        sizePolicy.setHeightForWidth(
            self.btn_autonom_docking.sizePolicy().hasHeightForWidth()
        )
        self.btn_autonom_docking.setSizePolicy(sizePolicy)
        self.btn_autonom_docking.setMinimumSize(QSize(0, 0))
        self.btn_autonom_docking.setFont(font)
        self.btn_autonom_docking.setCursor(QCursor(Qt.PointingHandCursor))
        self.start_transect = QPushButton(Form)
        self.start_transect.setObjectName(u"start_transect")
        self.start_transect.setGeometry(QRect(10, 160, 431, 47))
        sizePolicy.setHeightForWidth(
            self.start_transect.sizePolicy().hasHeightForWidth()
        )
        self.start_transect.setSizePolicy(sizePolicy)
        self.start_transect.setMinimumSize(QSize(0, 0))
        self.start_transect.setFont(font)
        self.start_transect.setCursor(QCursor(Qt.PointingHandCursor))
        self.title_effektforbruk = QLabel(Form)
        self.title_effektforbruk.setObjectName(u"title_effektforbruk")
        self.title_effektforbruk.setGeometry(QRect(20, 220, 191, 18))
        self.title_effektforbruk.setMinimumSize(QSize(0, 0))
        self.title_effektforbruk.setMaximumSize(QSize(16777215, 16777215))
        self.title_effektforbruk.setFont(font)
        self.title_effektforbruk.setStyleSheet(u"")
        self.text_effekt_elektronikk = QLabel(Form)
        self.text_effekt_elektronikk.setObjectName(u"text_effekt_elektronikk")
        self.text_effekt_elektronikk.setGeometry(QRect(20, 240, 113, 42))
        self.text_effekt_elektronikk.setMinimumSize(QSize(0, 0))
        self.text_effekt_elektronikk.setMaximumSize(QSize(16777215, 16777215))
        self.text_effekt_elektronikk.setFont(font)
        self.text_effekt_elektronikk.setTextFormat(Qt.RichText)
        self.text_effekt_thrustere = QLabel(Form)
        self.text_effekt_thrustere.setObjectName(u"text_effekt_thrustere")
        self.text_effekt_thrustere.setGeometry(QRect(20, 280, 113, 42))
        self.text_effekt_thrustere.setMinimumSize(QSize(0, 0))
        self.text_effekt_thrustere.setMaximumSize(QSize(16777215, 16777215))
        self.text_effekt_thrustere.setFont(font)
        self.text_effekt_thrustere.setTextFormat(Qt.PlainText)
        self.text_effekt_manipulator = QLabel(Form)
        self.text_effekt_manipulator.setObjectName(u"text_effekt_manipulator")
        self.text_effekt_manipulator.setGeometry(QRect(20, 320, 113, 42))
        self.text_effekt_manipulator.setMinimumSize(QSize(0, 0))
        self.text_effekt_manipulator.setMaximumSize(QSize(16777215, 16777215))
        self.text_effekt_manipulator.setFont(font)
        self.text_effekt_manipulator.setTextFormat(Qt.RichText)
        self.label_effekt_elektronikk = QLabel(Form)
        self.label_effekt_elektronikk.setObjectName(u"label_effekt_elektronikk")
        self.label_effekt_elektronikk.setGeometry(QRect(140, 240, 74, 42))
        self.label_effekt_elektronikk.setMinimumSize(QSize(0, 0))
        self.label_effekt_elektronikk.setMaximumSize(QSize(16777215, 16777215))
        self.label_effekt_elektronikk.setFont(font)
        self.label_effekt_elektronikk.setFrameShape(QFrame.NoFrame)
        self.label_effekt_elektronikk.setLineWidth(0)
        self.label_effekt_elektronikk.setMidLineWidth(0)
        self.label_effekt_elektronikk.setAlignment(Qt.AlignCenter)
        self.label_effekt_elektronikk.setMargin(0)
        self.label_effekt_thrustere = QLabel(Form)
        self.label_effekt_thrustere.setObjectName(u"label_effekt_thrustere")
        self.label_effekt_thrustere.setGeometry(QRect(140, 280, 74, 42))
        self.label_effekt_thrustere.setMinimumSize(QSize(0, 0))
        self.label_effekt_thrustere.setMaximumSize(QSize(16777215, 16777215))
        self.label_effekt_thrustere.setFont(font)
        self.label_effekt_thrustere.setFrameShape(QFrame.NoFrame)
        self.label_effekt_thrustere.setLineWidth(0)
        self.label_effekt_thrustere.setMidLineWidth(0)
        self.label_effekt_thrustere.setAlignment(Qt.AlignCenter)
        self.label_effekt_thrustere.setMargin(0)
        self.label_effekt_manipulator = QLabel(Form)
        self.label_effekt_manipulator.setObjectName(u"label_effekt_manipulator")
        self.label_effekt_manipulator.setGeometry(QRect(140, 320, 74, 42))
        self.label_effekt_manipulator.setMinimumSize(QSize(0, 0))
        self.label_effekt_manipulator.setMaximumSize(QSize(16777215, 16777215))
        self.label_effekt_manipulator.setFont(font)
        self.label_effekt_manipulator.setFrameShape(QFrame.NoFrame)
        self.label_effekt_manipulator.setLineWidth(0)
        self.label_effekt_manipulator.setMidLineWidth(0)
        self.label_effekt_manipulator.setAlignment(Qt.AlignCenter)
        self.label_effekt_manipulator.setMargin(0)
        self.title_temp_ROV = QLabel(Form)
        self.title_temp_ROV.setObjectName(u"title_temp_ROV")
        self.title_temp_ROV.setGeometry(QRect(260, 220, 171, 18))
        self.title_temp_ROV.setMaximumSize(QSize(16777215, 16777215))
        self.title_temp_ROV.setFont(font)
        self.title_temp_ROV.setTextFormat(Qt.PlainText)
        self.text_hovedkort = QLabel(Form)
        self.text_hovedkort.setObjectName(u"text_hovedkort")
        self.text_hovedkort.setGeometry(QRect(260, 240, 113, 38))
        self.text_hovedkort.setMinimumSize(QSize(0, 0))
        self.text_hovedkort.setMaximumSize(QSize(16777215, 16777215))
        self.text_hovedkort.setFont(font)
        self.text_hovedkort.setTextFormat(Qt.PlainText)
        self.text_hovedkort.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter
        )
        self.label_temp_ROV_hovedkort = QLabel(Form)
        self.label_temp_ROV_hovedkort.setObjectName(u"label_temp_ROV_hovedkort")
        self.label_temp_ROV_hovedkort.setGeometry(QRect(380, 240, 74, 38))
        self.label_temp_ROV_hovedkort.setMinimumSize(QSize(0, 0))
        self.label_temp_ROV_hovedkort.setMaximumSize(QSize(16777215, 16777215))
        self.label_temp_ROV_hovedkort.setFont(font)
        self.label_temp_ROV_hovedkort.setFrameShape(QFrame.NoFrame)
        self.label_temp_ROV_hovedkort.setLineWidth(0)
        self.label_temp_ROV_hovedkort.setMidLineWidth(0)
        self.label_temp_ROV_hovedkort.setAlignment(Qt.AlignCenter)
        self.label_temp_ROV_hovedkort.setMargin(0)
        self.text_kraftkort = QLabel(Form)
        self.text_kraftkort.setObjectName(u"text_kraftkort")
        self.text_kraftkort.setGeometry(QRect(260, 280, 113, 38))
        self.text_kraftkort.setMinimumSize(QSize(0, 0))
        self.text_kraftkort.setFont(font)
        self.text_kraftkort.setTextFormat(Qt.RichText)
        self.text_sensorkort = QLabel(Form)
        self.text_sensorkort.setObjectName(u"text_sensorkort")
        self.text_sensorkort.setGeometry(QRect(260, 320, 113, 38))
        self.text_sensorkort.setMinimumSize(QSize(0, 0))
        self.text_sensorkort.setFont(font)
        self.text_sensorkort.setTextFormat(Qt.RichText)
        self.label_temp_ROV_kraftkort = QLabel(Form)
        self.label_temp_ROV_kraftkort.setObjectName(u"label_temp_ROV_kraftkort")
        self.label_temp_ROV_kraftkort.setGeometry(QRect(380, 280, 74, 38))
        self.label_temp_ROV_kraftkort.setMinimumSize(QSize(0, 0))
        self.label_temp_ROV_kraftkort.setMaximumSize(QSize(16777215, 16777215))
        self.label_temp_ROV_kraftkort.setFont(font)
        self.label_temp_ROV_kraftkort.setFrameShape(QFrame.NoFrame)
        self.label_temp_ROV_kraftkort.setLineWidth(0)
        self.label_temp_ROV_kraftkort.setMidLineWidth(0)
        self.label_temp_ROV_kraftkort.setAlignment(Qt.AlignCenter)
        self.label_temp_ROV_kraftkort.setMargin(0)
        self.label_temp_ROV_sensorkort = QLabel(Form)
        self.label_temp_ROV_sensorkort.setObjectName(u"label_temp_ROV_sensorkort")
        self.label_temp_ROV_sensorkort.setGeometry(QRect(380, 320, 74, 38))
        self.label_temp_ROV_sensorkort.setMinimumSize(QSize(0, 0))
        self.label_temp_ROV_sensorkort.setMaximumSize(QSize(16777215, 16777215))
        self.label_temp_ROV_sensorkort.setFont(font)
        self.label_temp_ROV_sensorkort.setFrameShape(QFrame.NoFrame)
        self.label_temp_ROV_sensorkort.setLineWidth(0)
        self.label_temp_ROV_sensorkort.setMidLineWidth(0)
        self.label_temp_ROV_sensorkort.setAlignment(Qt.AlignCenter)
        self.label_temp_ROV_sensorkort.setMargin(0)
        self.title_motor = QLabel(Form)
        self.title_motor.setObjectName(u"title_motor")
        self.title_motor.setGeometry(QRect(490, 10, 421, 18))
        self.title_motor.setFont(font)
        self.text_rov = QLabel(Form)
        self.text_rov.setObjectName(u"text_rov")
        self.text_rov.setGeometry(QRect(490, 30, 357, 14))
        font1 = QFont()
        font1.setPointSize(10)
        self.text_rov.setFont(font1)
        self.text_rov.setStyleSheet(u"color: rgb(113, 126, 149);")
        self.text_rov.setLineWidth(1)
        self.text_rov.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.img_manipulator_2 = QLabel(Form)
        self.img_manipulator_2.setObjectName(u"img_manipulator_2")
        self.img_manipulator_2.setGeometry(QRect(500, 50, 280, 330))
        sizePolicy.setHeightForWidth(
            self.img_manipulator_2.sizePolicy().hasHeightForWidth()
        )
        self.img_manipulator_2.setSizePolicy(sizePolicy)
        self.img_manipulator_2.setMinimumSize(QSize(0, 0))
        self.img_manipulator_2.setMaximumSize(QSize(16777215, 16777215))
        self.img_manipulator_2.setSizeIncrement(QSize(0, 0))
        self.img_manipulator_2.setAutoFillBackground(False)
        self.img_manipulator_2.setStyleSheet(u"")
        self.img_manipulator_2.setPixmap(QPixmap(u":/images/images/motorpaadrag.png"))
        self.img_manipulator_2.setScaledContents(True)
        self.img_manipulator_2.setAlignment(Qt.AlignCenter)
        self.img_manipulator_2.setMargin(0)
        self.title_kjoremodus = QLabel(Form)
        self.title_kjoremodus.setObjectName(u"title_kjoremodus")
        self.title_kjoremodus.setGeometry(QRect(20, 10, 371, 46))
        self.title_kjoremodus.setMinimumSize(QSize(0, 0))
        self.title_kjoremodus.setMaximumSize(QSize(16777215, 16777215))
        self.title_kjoremodus.setFont(font)
        self.title_kjoremodus.setStyleSheet(u"")
        self.img_manipulator = QLabel(Form)
        self.img_manipulator.setObjectName(u"img_manipulator")
        self.img_manipulator.setGeometry(QRect(70, 440, 320, 161))
        self.img_manipulator.setMinimumSize(QSize(0, 0))
        self.img_manipulator.setMaximumSize(QSize(16777215, 16777215))
        self.img_manipulator.setSizeIncrement(QSize(0, 0))
        self.img_manipulator.setPixmap(QPixmap(u":/images/images/manipulator.png"))
        self.img_manipulator.setScaledContents(True)
        self.lys_title = QLabel(Form)
        self.lys_title.setObjectName(u"lys_title")
        self.lys_title.setGeometry(QRect(490, 380, 123, 18))
        self.lys_title.setMinimumSize(QSize(0, 0))
        self.lys_title.setMaximumSize(QSize(16777215, 16777215))
        self.lys_title.setFont(font)
        self.lys_title.setTextFormat(Qt.PlainText)
        self.text_lys_forward = QLabel(Form)
        self.text_lys_forward.setObjectName(u"text_lys_forward")
        self.text_lys_forward.setGeometry(QRect(500, 400, 123, 68))
        self.text_lys_forward.setMinimumSize(QSize(0, 0))
        self.text_lys_forward.setMaximumSize(QSize(16777215, 16777215))
        self.text_lys_forward.setFont(font)
        self.text_lys_forward.setStyleSheet(u"color: rgb(113, 126, 149);")
        self.text_lys_forward.setTextFormat(Qt.RichText)
        self.slider_lys_forward = QSlider(Form)
        self.slider_lys_forward.setObjectName(u"slider_lys_forward")
        self.slider_lys_forward.setGeometry(QRect(600, 400, 124, 68))
        sizePolicy.setHeightForWidth(
            self.slider_lys_forward.sizePolicy().hasHeightForWidth()
        )
        self.slider_lys_forward.setSizePolicy(sizePolicy)
        self.slider_lys_forward.setMinimumSize(QSize(0, 68))
        self.slider_lys_forward.setMaximumSize(QSize(16777215, 68))
        self.slider_lys_forward.setFont(font)
        self.slider_lys_forward.setStyleSheet(u"")
        self.slider_lys_forward.setMaximum(100)
        self.slider_lys_forward.setOrientation(Qt.Horizontal)
        self.slider_lys_forward.setInvertedAppearance(False)
        self.slider_lys_forward.setInvertedControls(False)
        self.slider_lys_forward.setTickPosition(QSlider.TicksBothSides)
        self.slider_lys_forward.setTickInterval(10)
        self.label_percentage_lys_forward = QLabel(Form)
        self.label_percentage_lys_forward.setObjectName(u"label_percentage_lys_forward")
        self.label_percentage_lys_forward.setGeometry(QRect(740, 420, 50, 30))
        font2 = QFont()
        font2.setPointSize(9)
        self.label_percentage_lys_forward.setFont(font2)
        self.label_percentage_lys_forward.setAutoFillBackground(False)
        self.label_percentage_lys_forward.setStyleSheet(u"background: transparent;")
        self.label_percentage_lys_forward.setScaledContents(False)
        self.label_percentage_lys_forward.setAlignment(Qt.AlignCenter)
        self.label_percentage_lys_forward.setWordWrap(False)
        self.text_lys_down = QLabel(Form)
        self.text_lys_down.setObjectName(u"text_lys_down")
        self.text_lys_down.setGeometry(QRect(500, 460, 123, 68))
        self.text_lys_down.setMinimumSize(QSize(0, 0))
        self.text_lys_down.setMaximumSize(QSize(16777215, 16777215))
        self.text_lys_down.setFont(font)
        self.text_lys_down.setStyleSheet(
            u"/*Copyright (c) DevSec Studio. All rights reserved.\n"
            "\n"
            "MIT License\n"
            "\n"
            "Permission is hereby granted, free of charge, to any person obtaining a copy\n"
            'of this software and associated documentation files (the "Software"), to deal\n'
            "in the Software without restriction, including without limitation the rights\n"
            "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n"
            "copies of the Software, and to permit persons to whom the Software is\n"
            "furnished to do so, subject to the following conditions:\n"
            "\n"
            "The above copyright notice and this permission notice shall be included in all\n"
            "copies or substantial portions of the Software.\n"
            "\n"
            "THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n"
            "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n"
            "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n"
            "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n"
            "LIABILITY, WHETHER IN AN ACT"
            "ION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n"
            "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n"
            "*/\n"
            "\n"
            "/*-----QWidget-----*/\n"
            "QWidget\n"
            "{\n"
            "    color: #aaa;\n"
            "    background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(57, 49, 68, 255),stop:1 rgba(110, 105, 118, 255));\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "/*-----QLabel-----*/\n"
            "QLabel\n"
            "{\n"
            "	background-color: transparent;\n"
            "	color: #fff;\n"
            "	\n"
            "}\n"
            "\n"
            "\n"
            "/*-----QMenuBar-----*/\n"
            "QMenuBar \n"
            "{\n"
            "    background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(110, 105, 118, 255),stop:1 rgba(57, 49, 68, 255));\n"
            "	color: #fff;\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "QMenuBar::item\n"
            "{\n"
            "    background-color: transparent;\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "QMenuBar::item:selected\n"
            "{\n"
            "    background-color: #444;\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "QMenuBar::item:pressed\n"
            "{\n"
            "    border: 1px solid #000;\n"
            "    background-color: #444;\n"
            "    margin-bottom:-1"
            "px;\n"
            "    padding-bottom:1px;\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "/*-----QMenu-----*/\n"
            "QMenu\n"
            "{\n"
            "    background-color: #444;\n"
            "    border: 1px solid #222;\n"
            "    padding: 4px;\n"
            "    padding-right: 0px;\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "QMenu::item\n"
            "{\n"
            "    background-color: transparent;\n"
            "    padding: 2px 20px 2px 20px;\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "QMenu::item:disabled\n"
            "{\n"
            "    color: #555;\n"
            "    background-color: transparent;\n"
            "    padding: 2px 20px 2px 20px;\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "QMenu::item:selected\n"
            "{\n"
            "    background-color: #55aaff;\n"
            "    color: #fff;\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "/*-----QToolTip-----*/\n"
            "QToolBar\n"
            "{\n"
            "	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(57, 49, 68, 255),stop:1 rgba(110, 105, 118, 255));\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "/*-----QToolTip-----*/\n"
            "QToolTip\n"
            "{\n"
            "    border: 1px solid #222;\n"
            "    background-color: #333;\n"
            "    color: #aaa;\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "/*-----QToolButton-----*/\n"
            "QToolButton\n"
            "{\n"
            "    col"
            "or: #b1b1b1;\n"
            "    background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(75, 165, 255, 255),stop:0.509615 rgba(119, 187, 255, 255),stop:1 rgba(72, 164, 255, 255));\n"
            "    border-width: 1px;\n"
            "    border-color: #1e1e1e;\n"
            "    border-style: solid;\n"
            "	margin-right: 2px;\n"
            "	padding: 3px;\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "QToolButton:pressed\n"
            "{\n"
            "    background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(65, 155, 245, 255),stop:0.509615 rgba(109, 177, 245, 255),stop:1 rgba(72, 164, 255, 255));\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "QToolButton:checked\n"
            "{\n"
            "    background-color: #9999ff;\n"
            "	border: none;\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "/*-----QLineEdit-----*/\n"
            "QLineEdit{\n"
            "	background-color: #fff;\n"
            "	color: #000;\n"
            "	selection-color: #fff;\n"
            "	selection-background-color: #507098;\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "/*-----QTreeView-----*/\n"
            "QTreeView\n"
            "{\n"
            "	background-color: #242526;\n"
            "   	show-decoration-selected: 0;\n"
            "   	selection-background-color: tra"
            "nsparent; /* Used on Mac */\n"
            "	alternate-background-color: #404040;\n"
            "	selection-color: #fff; /* Used on Mac */\n"
            "	font: 8pt;\n"
            "	color: #fff;\n"
            "	outline : 0;\n"
            "\n"
            "}\n"
            "\n"
            "QTreeView::item\n"
            "{\n"
            "	border-top-color: transparent;\n"
            "	border-bottom-color: transparent;\n"
            "\n"
            "}\n"
            "\n"
            "QTreeView::item:hover\n"
            "{\n"
            "	background-color: #1a1b1c;\n"
            "	show-decoration-selected: 1;\n"
            "	color: #fff;\n"
            "\n"
            "}\n"
            "\n"
            "QTreeView::item:selected\n"
            "{\n"
            "	background-color: #41cd52;\n"
            "	color: #fff;\n"
            "\n"
            "}\n"
            "\n"
            "QTreeView::item:selected:active\n"
            "{\n"
            "	background-color: rgba(57, 49, 68, 255);\n"
            "	color: #fff;\n"
            "\n"
            "}\n"
            "\n"
            "QTreeView::item:selected:!active\n"
            "{\n"
            "	background-color: rgba(57, 49, 68, 255);\n"
            "	color: #fff;\n"
            "\n"
            "}\n"
            "\n"
            "QTreeView::branch:has-children:!has-siblings:closed,\n"
            "QTreeView::branch:closed:has-children:has-siblings\n"
            "{\n"
            "	border-image: none;\n"
            "	image: url(://tree-closed.png); /*To replace*/\n"
            "\n"
            "}\n"
            "\n"
            "QTreeView::branch:open:has-chil"
            "dren:!has-siblings,\n"
            "QTreeView::branch:open:has-children:has-siblings\n"
            "{\n"
            "	border-image: none;\n"
            "	image: url(://tree-open.png); /*To replace*/\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "/*-----QScrollBar-----*/\n"
            "QScrollBar:horizontal \n"
            "{\n"
            "    background-color: #333;\n"
            "    height: 8px;\n"
            "    margin: 0px;\n"
            "    padding: 0px;\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "QScrollBar::handle:horizontal \n"
            "{\n"
            "    border: 1px solid #111;\n"
            "    background-color: #535353;\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal,\n"
            "QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal \n"
            "{\n"
            "    width: 0px;\n"
            "    background-color: transparent;\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "QScrollBar:vertical \n"
            "{\n"
            "    background-color: #333;\n"
            "    width: 8px;\n"
            "    margin: 0;\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "QScrollBar::handle:vertical \n"
            "{\n"
            "    border: 1px solid #111;\n"
            "    background-color: #535353;\n"
            "\n"
            "}\n"
            "\n"
            "\n"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,\n"
            ""
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical \n"
            "{\n"
            "    height: 0px;\n"
            "    background-color: transparent;\n"
            "\n"
            "}\n"
            "\n"
            ""
        )
        self.text_lys_down.setTextFormat(Qt.RichText)
        self.slider_lys_down = QSlider(Form)
        self.slider_lys_down.setObjectName(u"slider_lys_down")
        self.slider_lys_down.setGeometry(QRect(600, 470, 124, 68))
        sizePolicy.setHeightForWidth(
            self.slider_lys_down.sizePolicy().hasHeightForWidth()
        )
        self.slider_lys_down.setSizePolicy(sizePolicy)
        self.slider_lys_down.setMinimumSize(QSize(0, 68))
        self.slider_lys_down.setMaximumSize(QSize(16777215, 68))
        self.slider_lys_down.setFont(font)
        self.slider_lys_down.setStyleSheet(u"")
        self.slider_lys_down.setMaximum(100)
        self.slider_lys_down.setOrientation(Qt.Horizontal)
        self.slider_lys_down.setInvertedAppearance(False)
        self.slider_lys_down.setInvertedControls(False)
        self.slider_lys_down.setTickPosition(QSlider.TicksBothSides)
        self.slider_lys_down.setTickInterval(10)
        self.label_percentage_lys_down = QLabel(Form)
        self.label_percentage_lys_down.setObjectName(u"label_percentage_lys_down")
        self.label_percentage_lys_down.setGeometry(QRect(740, 480, 50, 30))
        self.label_percentage_lys_down.setFont(font2)
        self.label_percentage_lys_down.setAutoFillBackground(False)
        self.label_percentage_lys_down.setStyleSheet(u"background: transparent;")
        self.label_percentage_lys_down.setScaledContents(False)
        self.label_percentage_lys_down.setAlignment(Qt.AlignCenter)
        self.label_percentage_lys_down.setWordWrap(False)
        self.label_percentage_mani_1 = QLabel(Form)
        self.label_percentage_mani_1.setObjectName(u"label_percentage_mani_1")
        self.label_percentage_mani_1.setGeometry(QRect(90, 510, 50, 30))
        self.label_percentage_mani_1.setFont(font2)
        self.label_percentage_mani_1.setAutoFillBackground(False)
        self.label_percentage_mani_1.setStyleSheet(u"background: transparent;")
        self.label_percentage_mani_1.setScaledContents(False)
        self.label_percentage_mani_1.setAlignment(Qt.AlignCenter)
        self.label_percentage_mani_1.setWordWrap(False)
        self.label_percentage_mani_3 = QLabel(Form)
        self.label_percentage_mani_3.setObjectName(u"label_percentage_mani_3")
        self.label_percentage_mani_3.setGeometry(QRect(160, 570, 50, 30))
        self.label_percentage_mani_3.setFont(font2)
        self.label_percentage_mani_3.setAutoFillBackground(False)
        self.label_percentage_mani_3.setStyleSheet(u"background: transparent;")
        self.label_percentage_mani_3.setScaledContents(False)
        self.label_percentage_mani_3.setAlignment(Qt.AlignCenter)
        self.label_percentage_mani_3.setWordWrap(False)
        self.label_percentage_mani_2 = QLabel(Form)
        self.label_percentage_mani_2.setObjectName(u"label_percentage_mani_2")
        self.label_percentage_mani_2.setGeometry(QRect(260, 440, 50, 30))
        self.label_percentage_mani_2.setFont(font2)
        self.label_percentage_mani_2.setAutoFillBackground(False)
        self.label_percentage_mani_2.setStyleSheet(u"background: transparent;")
        self.label_percentage_mani_2.setScaledContents(False)
        self.label_percentage_mani_2.setAlignment(Qt.AlignCenter)
        self.label_percentage_mani_2.setWordWrap(False)
        self.text_manipulator = QLabel(Form)
        self.text_manipulator.setObjectName(u"text_manipulator")
        self.text_manipulator.setGeometry(QRect(10, 410, 376, 34))
        self.text_manipulator.setFont(font1)
        self.text_manipulator.setStyleSheet(u"color: rgb(113, 126, 149);")
        self.text_manipulator.setLineWidth(1)
        self.text_manipulator.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter
        )
        self.text_manipulator.setMargin(10)
        self.label_gjsnitt_temp_ROV = QLabel(Form)
        self.label_gjsnitt_temp_ROV.setObjectName(u"label_gjsnitt_temp_ROV")
        self.label_gjsnitt_temp_ROV.setGeometry(QRect(150, 360, 58, 38))
        self.label_gjsnitt_temp_ROV.setMinimumSize(QSize(0, 0))
        self.label_gjsnitt_temp_ROV.setMaximumSize(QSize(16777215, 16777215))
        self.label_gjsnitt_temp_ROV.setFont(font)
        self.label_gjsnitt_temp_ROV.setFrameShape(QFrame.NoFrame)
        self.label_gjsnitt_temp_ROV.setLineWidth(0)
        self.label_gjsnitt_temp_ROV.setMidLineWidth(0)
        self.label_gjsnitt_temp_ROV.setAlignment(Qt.AlignCenter)
        self.label_gjsnitt_temp_ROV.setMargin(0)
        self.text_gjsnitttemp = QLabel(Form)
        self.text_gjsnitttemp.setObjectName(u"text_gjsnitttemp")
        self.text_gjsnitttemp.setGeometry(QRect(20, 360, 58, 38))
        self.text_gjsnitttemp.setMinimumSize(QSize(0, 0))
        self.text_gjsnitttemp.setMaximumSize(QSize(16777215, 16777215))
        self.text_gjsnitttemp.setFont(font)
        self.text_gjsnitttemp.setTextFormat(Qt.PlainText)
        self.text_gjsnitttemp.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter
        )
        self.thrust_label_1 = QLabel(Form)
        self.thrust_label_1.setObjectName(u"thrust_label_1")
        self.thrust_label_1.setGeometry(QRect(550, 60, 61, 51))
        self.thrust_label_5 = QLabel(Form)
        self.thrust_label_5.setObjectName(u"thrust_label_5")
        self.thrust_label_5.setGeometry(QRect(550, 110, 61, 51))
        self.thrust_label_8 = QLabel(Form)
        self.thrust_label_8.setObjectName(u"thrust_label_8")
        self.thrust_label_8.setGeometry(QRect(780, 110, 61, 51))
        self.thrust_label_2 = QLabel(Form)
        self.thrust_label_2.setObjectName(u"thrust_label_2")
        self.thrust_label_2.setGeometry(QRect(630, 60, 61, 51))
        self.thrust_label_6 = QLabel(Form)
        self.thrust_label_6.setObjectName(u"thrust_label_6")
        self.thrust_label_6.setGeometry(QRect(630, 110, 61, 51))
        self.thrust_label_7 = QLabel(Form)
        self.thrust_label_7.setObjectName(u"thrust_label_7")
        self.thrust_label_7.setGeometry(QRect(700, 110, 61, 51))
        self.thrust_label_3 = QLabel(Form)
        self.thrust_label_3.setObjectName(u"thrust_label_3")
        self.thrust_label_3.setGeometry(QRect(700, 60, 61, 51))
        self.thrust_label_4 = QLabel(Form)
        self.thrust_label_4.setObjectName(u"thrust_label_4")
        self.thrust_label_4.setGeometry(QRect(780, 60, 61, 51))
        self.knappen = QPushButton(Form)
        self.knappen.setObjectName(u"knappen")
        self.knappen.setGeometry(QRect(570, 270, 93, 28))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.btn1.setText(
            QCoreApplication.translate("Form", u"Manuell kj\u00f8ring", None)
        )
        self.btn_autonom_docking.setText(
            QCoreApplication.translate("Form", u"Autonom docking", None)
        )
        self.start_transect.setText(
            QCoreApplication.translate("Form", u"Start transect", None)
        )
        self.title_effektforbruk.setText(
            QCoreApplication.translate("Form", u"EFFEKTFORBRUK", None)
        )
        self.text_effekt_elektronikk.setText(
            QCoreApplication.translate("Form", u"Elektronikk:", None)
        )
        self.text_effekt_elektronikk.setProperty(
            "colorStyle", QCoreApplication.translate("Form", u"subTitle", None)
        )
        self.text_effekt_thrustere.setText(
            QCoreApplication.translate("Form", u"Thrustere:", None)
        )
        self.text_effekt_thrustere.setProperty(
            "colorStyle", QCoreApplication.translate("Form", u"subTitle", None)
        )
        self.text_effekt_manipulator.setText(
            QCoreApplication.translate("Form", u"Manipulator:", None)
        )
        self.text_effekt_manipulator.setProperty(
            "colorStyle", QCoreApplication.translate("Form", u"subTitle", None)
        )
        self.label_effekt_elektronikk.setText(
            QCoreApplication.translate("Form", u"---", None)
        )
        self.label_effekt_elektronikk.setProperty(
            "labelStyle", QCoreApplication.translate("Form", u"blackBg", None)
        )
        self.label_effekt_elektronikk.setProperty(
            "labelStyle2", QCoreApplication.translate("Form", u"whiteBg", None)
        )
        self.label_effekt_thrustere.setText(
            QCoreApplication.translate("Form", u"---", None)
        )
        self.label_effekt_thrustere.setProperty(
            "labelStyle", QCoreApplication.translate("Form", u"blackBg", None)
        )
        self.label_effekt_thrustere.setProperty(
            "labelStyle2", QCoreApplication.translate("Form", u"whiteBg", None)
        )
        self.label_effekt_manipulator.setText(
            QCoreApplication.translate("Form", u"---", None)
        )
        self.label_effekt_manipulator.setProperty(
            "labelStyle", QCoreApplication.translate("Form", u"blackBg", None)
        )
        self.label_effekt_manipulator.setProperty(
            "labelStyle2", QCoreApplication.translate("Form", u"whiteBg", None)
        )
        self.title_temp_ROV.setText(
            QCoreApplication.translate("Form", u"TEMPERATUR I ROV", None)
        )
        self.text_hovedkort.setText(
            QCoreApplication.translate("Form", u"Hovedkort:", None)
        )
        self.text_hovedkort.setProperty(
            "colorStyle", QCoreApplication.translate("Form", u"subTitle", None)
        )
        self.label_temp_ROV_hovedkort.setText(
            QCoreApplication.translate("Form", u"---", None)
        )
        self.label_temp_ROV_hovedkort.setProperty(
            "labelStyle", QCoreApplication.translate("Form", u"blackBg", None)
        )
        self.label_temp_ROV_hovedkort.setProperty(
            "labelStyle2", QCoreApplication.translate("Form", u"whiteBg", None)
        )
        self.text_kraftkort.setText(
            QCoreApplication.translate("Form", u"Kraftkort:", None)
        )
        self.text_kraftkort.setProperty(
            "colorStyle", QCoreApplication.translate("Form", u"subTitle", None)
        )
        self.text_sensorkort.setText(
            QCoreApplication.translate("Form", u"Sensorkort:", None)
        )
        self.text_sensorkort.setProperty(
            "colorStyle", QCoreApplication.translate("Form", u"subTitle", None)
        )
        self.label_temp_ROV_kraftkort.setText(
            QCoreApplication.translate("Form", u"---", None)
        )
        self.label_temp_ROV_kraftkort.setProperty(
            "labelStyle", QCoreApplication.translate("Form", u"blackBg", None)
        )
        self.label_temp_ROV_kraftkort.setProperty(
            "labelStyle2", QCoreApplication.translate("Form", u"whiteBg", None)
        )
        self.label_temp_ROV_sensorkort.setText(
            QCoreApplication.translate("Form", u"---", None)
        )
        self.label_temp_ROV_sensorkort.setProperty(
            "labelStyle", QCoreApplication.translate("Form", u"blackBg", None)
        )
        self.label_temp_ROV_sensorkort.setProperty(
            "labelStyle2", QCoreApplication.translate("Form", u"whiteBg", None)
        )
        self.title_motor.setText(
            QCoreApplication.translate("Form", u"MOTORP\u00c5DRAG", None)
        )
        self.text_rov.setText(QCoreApplication.translate("Form", u"ROV", None))
        self.text_rov.setProperty(
            "colorStyle", QCoreApplication.translate("Form", u"subTitle", None)
        )
        self.img_manipulator_2.setText("")
        self.title_kjoremodus.setText(
            QCoreApplication.translate("Form", u"KJ\u00d8REMODUS", None)
        )
        self.img_manipulator.setText("")
        self.lys_title.setText(QCoreApplication.translate("Form", u"LYS", None))
        self.text_lys_forward.setText(
            QCoreApplication.translate("Form", u"Frontlys:", None)
        )
        self.text_lys_forward.setProperty(
            "colorStyle", QCoreApplication.translate("Form", u"subTitle", None)
        )
        self.label_percentage_lys_forward.setText(
            QCoreApplication.translate(
                "Form",
                u'<html><head/><body><span>0</span><span style="vertical-align:super;">%</span></body></html>',
                None,
            )
        )
        self.text_lys_down.setText(
            QCoreApplication.translate("Form", u"Havbunnslys:", None)
        )
        self.text_lys_down.setProperty(
            "colorStyle", QCoreApplication.translate("Form", u"subTitle", None)
        )
        self.label_percentage_lys_down.setText(
            QCoreApplication.translate(
                "Form",
                u'<html><head/><body><span>0</span><span style="vertical-align:super;">%</span></body></html>',
                None,
            )
        )
        self.label_percentage_mani_1.setText(
            QCoreApplication.translate(
                "Form",
                u'<html><head/><body><span>0</span><span style="vertical-align:super;">%</span></body></html>',
                None,
            )
        )
        self.label_percentage_mani_3.setText(
            QCoreApplication.translate(
                "Form",
                u'<html><head/><body><span>0</span><span style="vertical-align:super;">%</span></body></html>',
                None,
            )
        )
        self.label_percentage_mani_2.setText(
            QCoreApplication.translate(
                "Form",
                u'<html><head/><body><span>0</span><span style="vertical-align:super;">%</span></body></html>',
                None,
            )
        )
        self.text_manipulator.setText(
            QCoreApplication.translate("Form", u"MANIPULATOR", None)
        )
        self.text_manipulator.setProperty(
            "colorStyle", QCoreApplication.translate("Form", u"subTitle", None)
        )
        self.label_gjsnitt_temp_ROV.setText(
            QCoreApplication.translate("Form", u"---", None)
        )
        self.label_gjsnitt_temp_ROV.setProperty(
            "labelStyle", QCoreApplication.translate("Form", u"blackBg", None)
        )
        self.label_gjsnitt_temp_ROV.setProperty(
            "labelStyle2", QCoreApplication.translate("Form", u"whiteBg", None)
        )
        self.text_gjsnitttemp.setText(
            QCoreApplication.translate("Form", u"Gj.snitt:", None)
        )
        self.text_gjsnitttemp.setProperty(
            "colorStyle", QCoreApplication.translate("Form", u"subTitle", None)
        )
        self.thrust_label_1.setText(
            QCoreApplication.translate("Form", u"----------", None)
        )
        self.thrust_label_5.setText(
            QCoreApplication.translate("Form", u"----------", None)
        )
        self.thrust_label_8.setText(
            QCoreApplication.translate("Form", u"----------", None)
        )
        self.thrust_label_2.setText(
            QCoreApplication.translate("Form", u"----------", None)
        )
        self.thrust_label_6.setText(
            QCoreApplication.translate("Form", u"----------", None)
        )
        self.thrust_label_7.setText(
            QCoreApplication.translate("Form", u"----------", None)
        )
        self.thrust_label_3.setText(
            QCoreApplication.translate("Form", u"----------", None)
        )
        self.thrust_label_4.setText(
            QCoreApplication.translate("Form", u"----------", None)
        )
        self.knappen.setText(QCoreApplication.translate("Form", u"PushButton", None))

    # retranslateUi
