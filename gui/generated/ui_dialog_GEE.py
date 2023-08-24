# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.resources\ui_BaseDialog_GEE.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_BaseDialog_GEE(object):
    def setupUi(self, BaseDialog_GEE):
        BaseDialog_GEE.setObjectName("BaseDialog_GEE")
        BaseDialog_GEE.resize(680, 570)
        BaseDialog_GEE.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        BaseDialog_GEE.setFocusPolicy(QtCore.Qt.NoFocus)
        BaseDialog_GEE.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/imgMapSWAT/images/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        BaseDialog_GEE.setWindowIcon(icon)
        BaseDialog_GEE.setStyleSheet("")
        BaseDialog_GEE.setSizeGripEnabled(False)
        self.labelOutlet = QtWidgets.QLabel(BaseDialog_GEE)
        self.labelOutlet.setGeometry(QtCore.QRect(20, 20, 211, 21))
        self.labelOutlet.setTextFormat(QtCore.Qt.RichText)
        self.labelOutlet.setObjectName("labelOutlet")
        self.labelDEM = QtWidgets.QLabel(BaseDialog_GEE)
        self.labelDEM.setGeometry(QtCore.QRect(50, 90, 91, 21))
        self.labelDEM.setTextFormat(QtCore.Qt.RichText)
        self.labelDEM.setObjectName("labelDEM")
        self.listView = QtWidgets.QListView(BaseDialog_GEE)
        self.listView.setGeometry(QtCore.QRect(0, 10, 681, 211))
        self.listView.setObjectName("listView")
        self.labelLanduse = QtWidgets.QLabel(BaseDialog_GEE)
        self.labelLanduse.setGeometry(QtCore.QRect(50, 120, 121, 21))
        self.labelLanduse.setTextFormat(QtCore.Qt.RichText)
        self.labelLanduse.setObjectName("labelLanduse")
        self.labelSoil = QtWidgets.QLabel(BaseDialog_GEE)
        self.labelSoil.setGeometry(QtCore.QRect(50, 150, 91, 21))
        self.labelSoil.setTextFormat(QtCore.Qt.RichText)
        self.labelSoil.setObjectName("labelSoil")
        self.lineX = QtWidgets.QLineEdit(BaseDialog_GEE)
        self.lineX.setGeometry(QtCore.QRect(250, 20, 91, 22))
        self.lineX.setAlignment(QtCore.Qt.AlignCenter)
        self.lineX.setObjectName("lineX")
        self.lineY = QtWidgets.QLineEdit(BaseDialog_GEE)
        self.lineY.setGeometry(QtCore.QRect(370, 20, 91, 22))
        self.lineY.setAlignment(QtCore.Qt.AlignCenter)
        self.lineY.setObjectName("lineY")
        self.labelX = QtWidgets.QLabel(BaseDialog_GEE)
        self.labelX.setGeometry(QtCore.QRect(230, 20, 21, 21))
        self.labelX.setTextFormat(QtCore.Qt.RichText)
        self.labelX.setObjectName("labelX")
        self.labelY = QtWidgets.QLabel(BaseDialog_GEE)
        self.labelY.setGeometry(QtCore.QRect(350, 20, 21, 21))
        self.labelY.setTextFormat(QtCore.Qt.RichText)
        self.labelY.setObjectName("labelY")
        self.mQgsProjection_Outlet = QgsProjectionSelectionWidget(BaseDialog_GEE)
        self.mQgsProjection_Outlet.setGeometry(QtCore.QRect(480, 20, 181, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.mQgsProjection_Outlet.setFont(font)
        self.mQgsProjection_Outlet.setObjectName("mQgsProjection_Outlet")
        self.labelSoilTargetCRS = QtWidgets.QLabel(BaseDialog_GEE)
        self.labelSoilTargetCRS.setGeometry(QtCore.QRect(20, 380, 281, 21))
        font = QtGui.QFont()
        font.setUnderline(False)
        self.labelSoilTargetCRS.setFont(font)
        self.labelSoilTargetCRS.setTextFormat(QtCore.Qt.RichText)
        self.labelSoilTargetCRS.setObjectName("labelSoilTargetCRS")
        self.mQgsProjection_Target = QgsProjectionSelectionWidget(BaseDialog_GEE)
        self.mQgsProjection_Target.setGeometry(QtCore.QRect(250, 380, 411, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.mQgsProjection_Target.setFont(font)
        self.mQgsProjection_Target.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.mQgsProjection_Target.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.mQgsProjection_Target.setObjectName("mQgsProjection_Target")
        self.pushButton_AddBasemap = QtWidgets.QPushButton(BaseDialog_GEE)
        self.pushButton_AddBasemap.setGeometry(QtCore.QRect(350, 50, 131, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_AddBasemap.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/imgMapSWAT/images/basemap.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_AddBasemap.setIcon(icon1)
        self.pushButton_AddBasemap.setObjectName("pushButton_AddBasemap")
        self.listView_3 = QtWidgets.QListView(BaseDialog_GEE)
        self.listView_3.setGeometry(QtCore.QRect(0, 230, 681, 131))
        self.listView_3.setObjectName("listView_3")
        self.checkBox_DEM = QtWidgets.QCheckBox(BaseDialog_GEE)
        self.checkBox_DEM.setGeometry(QtCore.QRect(20, 90, 21, 20))
        self.checkBox_DEM.setText("")
        self.checkBox_DEM.setObjectName("checkBox_DEM")
        self.checkBox_Landuse = QtWidgets.QCheckBox(BaseDialog_GEE)
        self.checkBox_Landuse.setGeometry(QtCore.QRect(20, 120, 21, 20))
        self.checkBox_Landuse.setText("")
        self.checkBox_Landuse.setObjectName("checkBox_Landuse")
        self.checkBox_Soil = QtWidgets.QCheckBox(BaseDialog_GEE)
        self.checkBox_Soil.setGeometry(QtCore.QRect(20, 150, 21, 20))
        self.checkBox_Soil.setText("")
        self.checkBox_Soil.setObjectName("checkBox_Soil")
        self.pushButton_MANUAL = QtWidgets.QPushButton(BaseDialog_GEE)
        self.pushButton_MANUAL.setGeometry(QtCore.QRect(20, 290, 151, 61))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_MANUAL.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/imgMapSWAT/images/shape.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_MANUAL.setIcon(icon2)
        self.pushButton_MANUAL.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_MANUAL.setObjectName("pushButton_MANUAL")
        self.pushButton_SHAPEFILE = QtWidgets.QPushButton(BaseDialog_GEE)
        self.pushButton_SHAPEFILE.setGeometry(QtCore.QRect(250, 290, 151, 61))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_SHAPEFILE.setFont(font)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/imgMapSWAT/images/upload.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_SHAPEFILE.setIcon(icon3)
        self.pushButton_SHAPEFILE.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_SHAPEFILE.setObjectName("pushButton_SHAPEFILE")
        self.pushButton_BUFFER = QtWidgets.QPushButton(BaseDialog_GEE)
        self.pushButton_BUFFER.setGeometry(QtCore.QRect(580, 260, 81, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_BUFFER.setFont(font)
        self.pushButton_BUFFER.setObjectName("pushButton_BUFFER")
        self.pushButton_SWATinputs = QtWidgets.QPushButton(BaseDialog_GEE)
        self.pushButton_SWATinputs.setGeometry(QtCore.QRect(170, 420, 321, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_SWATinputs.setFont(font)
        self.pushButton_SWATinputs.setObjectName("pushButton_SWATinputs")
        self.listView_4 = QtWidgets.QListView(BaseDialog_GEE)
        self.listView_4.setGeometry(QtCore.QRect(0, 370, 681, 111))
        self.listView_4.setObjectName("listView_4")
        self.labelSoilClipping = QtWidgets.QLabel(BaseDialog_GEE)
        self.labelSoilClipping.setGeometry(QtCore.QRect(20, 240, 241, 21))
        font = QtGui.QFont()
        font.setUnderline(False)
        self.labelSoilClipping.setFont(font)
        self.labelSoilClipping.setTextFormat(QtCore.Qt.RichText)
        self.labelSoilClipping.setObjectName("labelSoilClipping")
        self.pushButton_Save = QtWidgets.QPushButton(BaseDialog_GEE)
        self.pushButton_Save.setGeometry(QtCore.QRect(462, 490, 101, 28))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_Save.setFont(font)
        self.pushButton_Save.setObjectName("pushButton_Save")
        self.pushButton_Close = QtWidgets.QPushButton(BaseDialog_GEE)
        self.pushButton_Close.setGeometry(QtCore.QRect(570, 490, 93, 28))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_Close.setFont(font)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/imgMapSWAT/images/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Close.setIcon(icon4)
        self.pushButton_Close.setObjectName("pushButton_Close")
        self.lineBuffer = QtWidgets.QLineEdit(BaseDialog_GEE)
        self.lineBuffer.setGeometry(QtCore.QRect(480, 260, 51, 41))
        self.lineBuffer.setAlignment(QtCore.Qt.AlignCenter)
        self.lineBuffer.setObjectName("lineBuffer")
        self.labelBuffer = QtWidgets.QLabel(BaseDialog_GEE)
        self.labelBuffer.setGeometry(QtCore.QRect(540, 270, 31, 21))
        self.labelBuffer.setTextFormat(QtCore.Qt.RichText)
        self.labelBuffer.setObjectName("labelBuffer")
        self.mQgsFileWidget_Polygon = QgsFileWidget(BaseDialog_GEE)
        self.mQgsFileWidget_Polygon.setGeometry(QtCore.QRect(240, 260, 201, 21))
        self.mQgsFileWidget_Polygon.setObjectName("mQgsFileWidget_Polygon")
        self.progressBar = QtWidgets.QProgressBar(BaseDialog_GEE)
        self.progressBar.setGeometry(QtCore.QRect(10, 490, 441, 21))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.pushButton_Info = QtWidgets.QPushButton(BaseDialog_GEE)
        self.pushButton_Info.setGeometry(QtCore.QRect(10, 530, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_Info.setFont(font)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/imgMapSWAT/images/info2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Info.setIcon(icon5)
        self.pushButton_Info.setObjectName("pushButton_Info")
        self.labelPath = QtWidgets.QLabel(BaseDialog_GEE)
        self.labelPath.setGeometry(QtCore.QRect(330, 540, 341, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        self.labelPath.setFont(font)
        self.labelPath.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.labelPath.setText("")
        self.labelPath.setTextFormat(QtCore.Qt.PlainText)
        self.labelPath.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelPath.setObjectName("labelPath")
        self.pushButton_point = QtWidgets.QPushButton(BaseDialog_GEE)
        self.pushButton_point.setGeometry(QtCore.QRect(160, 50, 121, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_point.setFont(font)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/imgMapSWAT/images/point.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_point.setIcon(icon6)
        self.pushButton_point.setObjectName("pushButton_point")
        self.comboBox_DEM = QtWidgets.QComboBox(BaseDialog_GEE)
        self.comboBox_DEM.setGeometry(QtCore.QRect(160, 90, 321, 22))
        self.comboBox_DEM.setObjectName("comboBox_DEM")
        self.comboBox_DEM.addItem("")
        self.comboBox_DEM.addItem("")
        self.comboBox_DEM.addItem("")
        self.comboBox_LANDUSE = QtWidgets.QComboBox(BaseDialog_GEE)
        self.comboBox_LANDUSE.setGeometry(QtCore.QRect(160, 120, 321, 22))
        self.comboBox_LANDUSE.setObjectName("comboBox_LANDUSE")
        self.comboBox_LANDUSE.addItem("")
        self.comboBox_LANDUSE.addItem("")
        self.comboBox_LANDUSE.addItem("")
        self.comboBox_LANDUSE.addItem("")
        self.comboBox_LANDUSE.addItem("")
        self.comboBox_LANDUSE.addItem("")
        self.comboBox_LANDUSE.addItem("")
        self.comboBox_SOIL = QtWidgets.QComboBox(BaseDialog_GEE)
        self.comboBox_SOIL.setGeometry(QtCore.QRect(160, 150, 321, 22))
        self.comboBox_SOIL.setObjectName("comboBox_SOIL")
        self.comboBox_SOIL.addItem("")
        self.label_3 = QtWidgets.QLabel(BaseDialog_GEE)
        self.label_3.setGeometry(QtCore.QRect(520, 60, 141, 131))
        self.label_3.setObjectName("label_3")
        self.pushButton_GetMaps = QtWidgets.QPushButton(BaseDialog_GEE)
        self.pushButton_GetMaps.setGeometry(QtCore.QRect(250, 180, 151, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_GetMaps.setFont(font)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/imgMapSWAT/images/world.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_GetMaps.setIcon(icon7)
        self.pushButton_GetMaps.setObjectName("pushButton_GetMaps")
        self.pushButton_AUTOBASIN = QtWidgets.QPushButton(BaseDialog_GEE)
        self.pushButton_AUTOBASIN.setGeometry(QtCore.QRect(480, 330, 181, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_AUTOBASIN.setFont(font)
        self.pushButton_AUTOBASIN.setObjectName("pushButton_AUTOBASIN")
        self.labelBuffer_2 = QtWidgets.QLabel(BaseDialog_GEE)
        self.labelBuffer_2.setGeometry(QtCore.QRect(480, 240, 101, 21))
        self.labelBuffer_2.setTextFormat(QtCore.Qt.RichText)
        self.labelBuffer_2.setObjectName("labelBuffer_2")
        self.comboBox_AUTOBASIN = QtWidgets.QComboBox(BaseDialog_GEE)
        self.comboBox_AUTOBASIN.setGeometry(QtCore.QRect(480, 310, 181, 20))
        self.comboBox_AUTOBASIN.setObjectName("comboBox_AUTOBASIN")
        self.comboBox_AUTOBASIN.addItem("")
        self.comboBox_AUTOBASIN.addItem("")
        self.comboBox_AUTOBASIN.addItem("")
        self.comboBox_AUTOBASIN.addItem("")
        self.comboBox_AUTOBASIN.addItem("")
        self.comboBox_AUTOBASIN.addItem("")
        self.pushButton_coffee = QtWidgets.QPushButton(BaseDialog_GEE)
        self.pushButton_coffee.setGeometry(QtCore.QRect(150, 530, 131, 31))
        self.pushButton_coffee.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/imgMapSWAT/images/coffee.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_coffee.setIcon(icon8)
        self.pushButton_coffee.setIconSize(QtCore.QSize(100, 30))
        self.pushButton_coffee.setObjectName("pushButton_coffee")
        self.labelCheck_coffee = QtWidgets.QLabel(BaseDialog_GEE)
        self.labelCheck_coffee.setGeometry(QtCore.QRect(280, 530, 31, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        self.labelCheck_coffee.setFont(font)
        self.labelCheck_coffee.setStyleSheet("color: rgb(0, 170, 0);")
        self.labelCheck_coffee.setText("")
        self.labelCheck_coffee.setTextFormat(QtCore.Qt.PlainText)
        self.labelCheck_coffee.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelCheck_coffee.setObjectName("labelCheck_coffee")
        self.pushButton_infoMaps = QtWidgets.QPushButton(BaseDialog_GEE)
        self.pushButton_infoMaps.setGeometry(QtCore.QRect(480, 90, 31, 21))
        self.pushButton_infoMaps.setText("")
        self.pushButton_infoMaps.setIcon(icon5)
        self.pushButton_infoMaps.setAutoDefault(False)
        self.pushButton_infoMaps.setFlat(True)
        self.pushButton_infoMaps.setObjectName("pushButton_infoMaps")
        self.pushButton_infoMaps_2 = QtWidgets.QPushButton(BaseDialog_GEE)
        self.pushButton_infoMaps_2.setGeometry(QtCore.QRect(480, 120, 31, 21))
        self.pushButton_infoMaps_2.setText("")
        self.pushButton_infoMaps_2.setIcon(icon5)
        self.pushButton_infoMaps_2.setAutoDefault(False)
        self.pushButton_infoMaps_2.setFlat(True)
        self.pushButton_infoMaps_2.setObjectName("pushButton_infoMaps_2")
        self.pushButton_infoMaps_3 = QtWidgets.QPushButton(BaseDialog_GEE)
        self.pushButton_infoMaps_3.setGeometry(QtCore.QRect(480, 150, 31, 21))
        self.pushButton_infoMaps_3.setText("")
        self.pushButton_infoMaps_3.setIcon(icon5)
        self.pushButton_infoMaps_3.setAutoDefault(False)
        self.pushButton_infoMaps_3.setFlat(True)
        self.pushButton_infoMaps_3.setObjectName("pushButton_infoMaps_3")
        self.labelOR = QtWidgets.QLabel(BaseDialog_GEE)
        self.labelOR.setGeometry(QtCore.QRect(300, 59, 31, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        self.labelOR.setFont(font)
        self.labelOR.setStyleSheet("color: rgb(0, 170, 0);")
        self.labelOR.setText("")
        self.labelOR.setTextFormat(QtCore.Qt.PlainText)
        self.labelOR.setPixmap(QtGui.QPixmap(":/imgMapSWAT/images/arrow.png"))
        self.labelOR.setScaledContents(True)
        self.labelOR.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelOR.setObjectName("labelOR")
        self.listView_4.raise_()
        self.listView.raise_()
        self.labelOutlet.raise_()
        self.labelDEM.raise_()
        self.labelLanduse.raise_()
        self.labelSoil.raise_()
        self.lineX.raise_()
        self.lineY.raise_()
        self.labelX.raise_()
        self.labelY.raise_()
        self.mQgsProjection_Outlet.raise_()
        self.labelSoilTargetCRS.raise_()
        self.mQgsProjection_Target.raise_()
        self.pushButton_AddBasemap.raise_()
        self.listView_3.raise_()
        self.checkBox_DEM.raise_()
        self.checkBox_Landuse.raise_()
        self.checkBox_Soil.raise_()
        self.pushButton_MANUAL.raise_()
        self.pushButton_SHAPEFILE.raise_()
        self.pushButton_BUFFER.raise_()
        self.pushButton_SWATinputs.raise_()
        self.labelSoilClipping.raise_()
        self.pushButton_Save.raise_()
        self.pushButton_Close.raise_()
        self.lineBuffer.raise_()
        self.labelBuffer.raise_()
        self.mQgsFileWidget_Polygon.raise_()
        self.progressBar.raise_()
        self.pushButton_Info.raise_()
        self.labelPath.raise_()
        self.pushButton_point.raise_()
        self.comboBox_DEM.raise_()
        self.comboBox_LANDUSE.raise_()
        self.comboBox_SOIL.raise_()
        self.label_3.raise_()
        self.pushButton_GetMaps.raise_()
        self.pushButton_AUTOBASIN.raise_()
        self.labelBuffer_2.raise_()
        self.comboBox_AUTOBASIN.raise_()
        self.pushButton_coffee.raise_()
        self.labelCheck_coffee.raise_()
        self.pushButton_infoMaps.raise_()
        self.pushButton_infoMaps_2.raise_()
        self.pushButton_infoMaps_3.raise_()
        self.labelOR.raise_()

        self.retranslateUi(BaseDialog_GEE)
        self.pushButton_Save.clicked.connect(BaseDialog_GEE.Open)
        self.pushButton_Close.clicked.connect(BaseDialog_GEE.Close)
        self.pushButton_Info.clicked.connect(BaseDialog_GEE.info)
        self.pushButton_point.clicked.connect(BaseDialog_GEE.AddOutlet)
        self.pushButton_AddBasemap.clicked.connect(BaseDialog_GEE.AddBasemap)
        self.pushButton_GetMaps.clicked.connect(BaseDialog_GEE.GetMaps)
        self.pushButton_MANUAL.clicked.connect(BaseDialog_GEE.Clip_New)
        self.pushButton_SHAPEFILE.clicked.connect(BaseDialog_GEE.Clip_Old)
        self.pushButton_BUFFER.clicked.connect(BaseDialog_GEE.Clip_Extension)
        self.pushButton_AUTOBASIN.clicked.connect(BaseDialog_GEE.Clip_Autobasin)
        self.pushButton_SWATinputs.clicked.connect(BaseDialog_GEE.CREATE_INPUTS)
        self.pushButton_coffee.clicked.connect(BaseDialog_GEE.coffee)
        self.pushButton_infoMaps.clicked.connect(BaseDialog_GEE.infoDEM)
        self.pushButton_infoMaps_2.clicked.connect(BaseDialog_GEE.infoLanduse)
        self.pushButton_infoMaps_3.clicked.connect(BaseDialog_GEE.infoSoil)
        QtCore.QMetaObject.connectSlotsByName(BaseDialog_GEE)

    def retranslateUi(self, BaseDialog_GEE):
        _translate = QtCore.QCoreApplication.translate
        BaseDialog_GEE.setWindowTitle(_translate("BaseDialog_GEE", "MapSWAT GEE"))
        self.labelOutlet.setText(_translate("BaseDialog_GEE", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">OUTLET Coordinates:</span></p></body></html>"))
        self.labelDEM.setText(_translate("BaseDialog_GEE", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">DEM:</span></p></body></html>"))
        self.labelLanduse.setText(_translate("BaseDialog_GEE", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">LANDUSE:</span></p></body></html>"))
        self.labelSoil.setText(_translate("BaseDialog_GEE", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">SOIL:</span></p></body></html>"))
        self.labelX.setText(_translate("BaseDialog_GEE", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">X</span></p></body></html>"))
        self.labelY.setText(_translate("BaseDialog_GEE", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">Y</span></p></body></html>"))
        self.labelSoilTargetCRS.setText(_translate("BaseDialog_GEE", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">SWAT INPUT MAPS CRS:</span></p></body></html>"))
        self.pushButton_AddBasemap.setText(_translate("BaseDialog_GEE", "ADD BASEMAP"))
        self.pushButton_MANUAL.setText(_translate("BaseDialog_GEE", "MANUAL\n"
" CLIP"))
        self.pushButton_SHAPEFILE.setText(_translate("BaseDialog_GEE", "SHAPEFILE\n"
" CLIP"))
        self.pushButton_BUFFER.setText(_translate("BaseDialog_GEE", "BUFFER\n"
" CLIP"))
        self.pushButton_SWATinputs.setText(_translate("BaseDialog_GEE", "CREATE SWAT INPUT MAPS"))
        self.labelSoilClipping.setText(_translate("BaseDialog_GEE", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">CLIPPING OPTIONS:</span></p></body></html>"))
        self.pushButton_Save.setText(_translate("BaseDialog_GEE", "OPEN FOLDER"))
        self.pushButton_Close.setText(_translate("BaseDialog_GEE", " CLOSE"))
        self.lineBuffer.setText(_translate("BaseDialog_GEE", "10"))
        self.labelBuffer.setText(_translate("BaseDialog_GEE", "<html><head/><body><p align=\"right\"><span style=\" font-weight:600;\">(Km)</span></p></body></html>"))
        self.pushButton_Info.setText(_translate("BaseDialog_GEE", " MapSWAT"))
        self.pushButton_point.setText(_translate("BaseDialog_GEE", "ADD OUTLET"))
        self.comboBox_DEM.setItemText(0, _translate("BaseDialog_GEE", "SRTM Digital Elevation Data 90m"))
        self.comboBox_DEM.setItemText(1, _translate("BaseDialog_GEE", "NASADEM Digital Elevation 30m"))
        self.comboBox_DEM.setItemText(2, _translate("BaseDialog_GEE", "Copernicus DEM GLO-30m"))
        self.comboBox_LANDUSE.setItemText(0, _translate("BaseDialog_GEE", "Copernicus Global Land Cover 2019"))
        self.comboBox_LANDUSE.setItemText(1, _translate("BaseDialog_GEE", "GlobCover: Global Land Cover Map 2009"))
        self.comboBox_LANDUSE.setItemText(2, _translate("BaseDialog_GEE", "Copernicus CORINE Land Cover 1990 (only Europe)"))
        self.comboBox_LANDUSE.setItemText(3, _translate("BaseDialog_GEE", "Copernicus CORINE Land Cover 2000 (only Europe)"))
        self.comboBox_LANDUSE.setItemText(4, _translate("BaseDialog_GEE", "Copernicus CORINE Land Cover 2006 (only Europe)"))
        self.comboBox_LANDUSE.setItemText(5, _translate("BaseDialog_GEE", "Copernicus CORINE Land Cover 2012 (only Europe)"))
        self.comboBox_LANDUSE.setItemText(6, _translate("BaseDialog_GEE", "Copernicus CORINE Land Cover 2018 (only Europe)"))
        self.comboBox_SOIL.setItemText(0, _translate("BaseDialog_GEE", "DSOLMap: Digital Soil Open Land Map"))
        self.label_3.setText(_translate("BaseDialog_GEE", "<html><head/><body><p><img src=\":/imgMapSWAT/images/MapSWAT_GEE.png\"/></p></body></html>"))
        self.pushButton_GetMaps.setText(_translate("BaseDialog_GEE", "GET MAPS"))
        self.pushButton_AUTOBASIN.setText(_translate("BaseDialog_GEE", "AUTOBASIN CLIP"))
        self.labelBuffer_2.setText(_translate("BaseDialog_GEE", "<html><head/><body><p><span style=\" font-weight:600; text-decoration: underline;\">FROM OUTLET:</span></p></body></html>"))
        self.comboBox_AUTOBASIN.setItemText(0, _translate("BaseDialog_GEE", "HydroSHEDS Basins L-7"))
        self.comboBox_AUTOBASIN.setItemText(1, _translate("BaseDialog_GEE", "HydroSHEDS Basins L-8"))
        self.comboBox_AUTOBASIN.setItemText(2, _translate("BaseDialog_GEE", "HydroSHEDS Basins L-9"))
        self.comboBox_AUTOBASIN.setItemText(3, _translate("BaseDialog_GEE", "HydroSHEDS Basins L-10"))
        self.comboBox_AUTOBASIN.setItemText(4, _translate("BaseDialog_GEE", "HydroSHEDS Basins L-11"))
        self.comboBox_AUTOBASIN.setItemText(5, _translate("BaseDialog_GEE", "HydroSHEDS Basins L-12"))

from qgsfilewidget import QgsFileWidget
from qgsprojectionselectionwidget import QgsProjectionSelectionWidget
from MapSWAT_v3.gui.generated import resources_rc
