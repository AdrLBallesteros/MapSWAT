# -*- coding: utf-8 -*-
"""
/***************************************************************************
 **MapSWAT
 **A QGIS plugin
 **Description: MapSWAT is a QGIS plugin for preparing SWAT or SWAT+ input maps.
----------------------------------------------------
       begin                : **January-2021
        copyright            : **COPYRIGHT
        email                : **alopez6@ucam.edu
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 3 of the License, or     *
 *   any later version.                                                    *
 *                                                                         *
 ***************************************************************************/
"""
import os.path
from qgis.core import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QAction
from .BaseDialog import BaseDialog
import MapSWAT_v3.gui.generated.resources_rc


class Base:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        self.action = QAction(
            QIcon(":/imgMapSWAT/images/icon.png"),
            "MapSWAT v3.0",
            self.iface.mainWindow(),
        )
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&MapSWAT v3.0", self.action)

    def unload(self):
        self.iface.removePluginMenu("&MapSWAT v3.0", self.action)
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        self.dlg = BaseDialog(self.iface)
        self.dlg.setWindowFlags(
            Qt.WindowSystemMenuHint
            | Qt.MSWindowsFixedSizeDialogHint
            | Qt.WindowTitleHint
            | Qt.WindowMinimizeButtonHint
        )
        # self.dlg.show()
        self.dlg.SelectionWindow()
        # self.dlg.InitialWindow()
        # self.dlg.exec_()
