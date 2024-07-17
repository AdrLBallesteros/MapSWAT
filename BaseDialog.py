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

from qgis.core import *
from qgis.gui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from MapSWAT_v3.gui.generated.ui_dialog import Ui_BaseDialog

from qgis.gui import QgsMapToolEmitPoint
from qgis.core import QgsProject, QgsRasterLayer
from PyQt5.QtCore import QFileInfo
from PyQt5.QtCore import QVariant
from PyQt5.QtGui import QColor
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import (
    QDialog,
    QMessageBox,
    QMainWindow,
    QApplication,
    QFileDialog,
    QPushButton,
    QInputDialog,
)

import os.path
import os
import processing
import shutil
import webbrowser
import csv
import json

from MapSWAT_v3.BaseDialog_GEE import BaseDialog_GEE


class BaseDialog(QDialog, Ui_BaseDialog):

    def __init__(self, iface):
        QDialog.__init__(self)
        self.setupUi(self)
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self.plugin_dir = os.path.dirname(os.path.abspath(__file__))

        # Change the CRS of the project to WGS84
        WGS84 = QgsCoordinateReferenceSystem(4326)
        QgsProject.instance().setCrs(WGS84)

        # Activate CRS selector and change default info.
        self.mQgsProjection_Outlet.setOptionVisible(
            self.mQgsProjection_Outlet.CrsNotSet, True
        )
        self.mQgsProjection_Outlet.setNotSetText("Select (X, Y) CRS")
        self.mQgsProjection_Target.setOptionVisible(
            self.mQgsProjection_Target.CrsNotSet, True
        )
        self.mQgsProjection_Target.setNotSetText(
            "Select target CRS for SWAT input maps"
        )

        # Filtering QGSFileWidget
        self.mQgsFileWidget_Polygon.setFilter("Shapefiles (*.shp)")
        self.mQgsFileWidget_DEM.setFilter(
            "TIFF files (*.tif);;ERDAS IMAGINE files (*.img)"
        )
        self.mQgsFileWidget_Landuse.setFilter(
            "TIFF files (*.tif);;ERDAS IMAGINE files (*.img)"
        )
        self.mQgsFileWidget_Soil.setFilter(
            "TIFF files (*.tif);;ERDAS IMAGINE files (*.img)"
        )

        # Enable button lock
        self.pushButton_NewPolygon.setEnabled(False)
        self.pushButton_OldPolygon.setEnabled(False)
        self.pushButton_Extension.setEnabled(False)
        self.pushButton_SWATinputs.setEnabled(False)

    def SelectionWindow(self):
        # Code to create a window to select the MapSWAT version
        msg2 = QMessageBox()
        msg2.setWindowIcon(QIcon(":/imgMapSWAT/images/icon2.png"))
        msg2.setWindowTitle("MapSWAT version")
        msg2.setText("Please, select the version of MapSWAT you want to use.")
        msg2.setDetailedText(
            "1. MapSWAT v3.0: \nThis is the standard version of MapSWAT. Users can import their own raster maps and prepare them in QSWAT or QSWAT+ format.  \n\n2. MapSWAT GEE: \nThis is the connected to Google Earth Engine (GEE) version of MapSWAT. Users must first sign up for a GEE account and install the GEE plugin from QGIS repository."
        )
        msg2.setTextFormat(Qt.RichText)

        # Create a custom button
        Button_v3 = QPushButton("MapSWAT v3.0")
        Button_GEE = QPushButton("MapSWAT GEE")
        font = Button_v3.font()
        font.setBold(True)
        Button_v3.setFont(font)
        font = Button_GEE.font()
        font.setBold(True)
        Button_GEE.setFont(font)
        msg2.addButton(Button_v3, QMessageBox.AcceptRole)  ##QMessageBox.ActionRole
        msg2.addButton(Button_GEE, QMessageBox.AcceptRole)

        # Show the QMessageBox()
        msg2.exec_()

        # Open MapSWAT v3 window
        if msg2.clickedButton() == Button_v3:
            self.show()
            self.InitialWindow()

        # Open MapSWAT GEE window
        elif msg2.clickedButton() == Button_GEE:

            plugin_path = os.path.abspath(__file__)
            plugin_directory = os.path.dirname(plugin_path)
            GEE_project_file = os.path.join(
                plugin_directory, "resources", "GEE_project_ID.json"
            )
            # Check if the GEE ID exists
            if os.path.exists(GEE_project_file):
                with open(GEE_project_file, "r") as file:
                    GEE_ID = json.load(file)
            # Enter the GEE project ID for ee.Initialize(project='my-project')
            if not os.path.exists(GEE_project_file):
                GEE_ID = QInputDialog.getText(
                    None,
                    "Earth Engine default project",
                    "Enter your GEE Cloud Project ID:",
                )
                with open(GEE_project_file, "w", encoding="utf-8") as file:
                    json.dump(GEE_ID, file)

            try:
                self.GEE = BaseDialog_GEE(self.iface)
                self.GEE.setWindowFlags(
                    Qt.WindowSystemMenuHint
                    | Qt.MSWindowsFixedSizeDialogHint
                    | Qt.WindowTitleHint
                    | Qt.WindowMinimizeButtonHint
                )
                # Call a function of the other class
                self.GEE.InitialWindow()
            except:
                fail = QMessageBox.warning(
                    None,
                    "Connection to Google Earth Engine (GEE) failed :(",
                    f"Please, make sure you have a good Internet connection and that you have entered your GEE Cloud Project ID correctly: *{GEE_ID[0]}*. If not, click [Ok] and enter your GEE Cloud Project ID again.",
                    QMessageBox.Ok,
                )
                if fail == QMessageBox.Ok:
                    # Rewrite GEE ID
                    GEE_ID = QInputDialog.getText(
                        None,
                        "Earth Engine default project",
                        "Enter your GEE Cloud Project ID again:",
                    )
                    with open(GEE_project_file, "w", encoding="utf-8") as file:
                        json.dump(GEE_ID, file)
                    self.close()
                else:
                    self.close()

    def InitialWindow(self):
        # Code to create a window to get the path of the MapSWAT project
        msg = QMessageBox()
        msg.setWindowIcon(QIcon(":/imgMapSWAT/images/icon2.png"))
        msg.setWindowTitle("Select Project Folder")
        msg.setText("Please, indicate a path to save the MapSWAT folder.")
        msg.setDetailedText(
            'Instructions: \n1. Click "OK" to create a new MapSWAT folder. \n2. Define the name of the new project folder.\n3. Save it.'
        )
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.No)

        if msg.exec_() == QMessageBox.Ok:
            try:
                # Get the new folder path
                filename = QtWidgets.QFileDialog.getSaveFileName(
                    self, "Define the name of the new project folder", "", ""
                )
                folder = str(filename[0])
                os.makedirs(folder)
                self.labelPath.setText(folder)

                path1 = folder + "\MapSWAT"
                os.makedirs(path1, exist_ok=True)
                path2 = folder + "\MapSWAT\WGS84"
                os.makedirs(path2, exist_ok=True)
                path3 = folder + "\MapSWAT\WGS84\CLIPPED"
                os.makedirs(path3, exist_ok=True)
                path4 = folder + "\MapSWAT\SWAT_INPUT_MAPS"
                os.makedirs(path4, exist_ok=True)
                path6 = folder + "\MapSWAT\SWAT_INPUT_MAPS\DEM"
                os.makedirs(path6, exist_ok=True)
                path7 = folder + "\MapSWAT\SWAT_INPUT_MAPS\LANDUSE"
                os.makedirs(path7, exist_ok=True)
                path8 = folder + "\MapSWAT\SWAT_INPUT_MAPS\SOIL"
                os.makedirs(path8, exist_ok=True)
                path9 = folder + "\MapSWAT\SWAT_INPUT_MAPS\INFO_GIS"
                os.makedirs(path9, exist_ok=True)
                path10 = folder + "\MapSWAT\SWAT_INPUT_MAPS\INFO_GIS\OUTLET"
                os.makedirs(path10, exist_ok=True)
                path11 = folder + "\MapSWAT\SWAT_INPUT_MAPS\INFO_GIS\POLYGON"
                os.makedirs(path11, exist_ok=True)
                path12 = folder + "\MapSWAT\SWAT_INPUT_MAPS\INFO_GIS\MERGE"
                os.makedirs(path12, exist_ok=True)

            except:
                self.close()
        else:
            self.close()

    def AddMaps(self):
        FolderPath = self.labelPath.text()

        self.progressBar.setValue(10)

        if self.checkBox_Soil.isChecked():
            # Reproject Soil to WGS84
            fileName = self.mQgsFileWidget_Soil.filePath()
            rlayer = QgsRasterLayer(fileName, "SOIL")
            crs_Soil = rlayer.crs()

            # Optimise map input process
            if crs_Soil == QgsCoordinateReferenceSystem("EPSG:4326"):
                rlayer = QgsRasterLayer(fileName, "SOIL")
                QgsProject.instance().addMapLayer(rlayer)

                self.pushButton_NewPolygon.setEnabled(True)
                self.pushButton_OldPolygon.setEnabled(True)
                self.pushButton_AddMaps.setEnabled(False)
                self.pushButton_MERGE.setEnabled(False)

            else:
                try:
                    # Reproject SOIL to WGS84
                    params = {
                        "INPUT": fileName,
                        "SOURCE_CRS": crs_Soil,
                        "TARGET_CRS": QgsCoordinateReferenceSystem("EPSG:4326"),
                        "RESAMPLING": 0,
                        "NODATA": None,
                        "TARGET_RESOLUTION": None,
                        "OPTIONS": "",
                        "DATA_TYPE": 0,
                        "TARGET_EXTENT": None,
                        "TARGET_EXTENT_CRS": None,
                        "MULTITHREADING": False,
                        "EXTRA": "",
                        "OUTPUT": FolderPath + "/MapSWAT/WGS84/SOIL.tif",
                    }
                    processing.run("gdal:warpreproject", params)

                    # Adding Soil to QGIS
                    fileName2 = FolderPath + "/MapSWAT/WGS84/SOIL.tif"
                    fileInfo = QFileInfo(fileName2)
                    baseName = fileInfo.baseName()
                    Soil = QgsRasterLayer(fileName2, baseName)
                    QgsProject.instance().addMapLayer(Soil)

                    self.pushButton_NewPolygon.setEnabled(True)
                    self.pushButton_OldPolygon.setEnabled(True)
                    self.pushButton_AddMaps.setEnabled(False)
                    self.pushButton_MERGE.setEnabled(False)

                except:
                    QMessageBox.warning(
                        None, "ADD LAYERS", "Please, select a raster layer in SOIL."
                    )

            self.progressBar.setValue(30)

        if self.checkBox_Landuse.isChecked():
            fileName = self.mQgsFileWidget_Landuse.filePath()
            rlayer = QgsRasterLayer(fileName, "LANDUSE")
            crs_Landuse = rlayer.crs()

            # Optimise map input process
            if crs_Landuse == QgsCoordinateReferenceSystem("EPSG:4326"):
                # Add Landuse to QGIS
                rlayer = QgsRasterLayer(fileName, "LANDUSE")
                QgsProject.instance().addMapLayer(rlayer)

                self.pushButton_NewPolygon.setEnabled(True)
                self.pushButton_OldPolygon.setEnabled(True)
                self.pushButton_AddMaps.setEnabled(False)
                self.pushButton_MERGE.setEnabled(False)

            else:
                try:
                    # Reproject Landuse to WGS84
                    params = {
                        "INPUT": fileName,
                        "SOURCE_CRS": crs_Landuse,
                        "TARGET_CRS": QgsCoordinateReferenceSystem("EPSG:4326"),
                        "RESAMPLING": 0,
                        "NODATA": None,
                        "TARGET_RESOLUTION": None,
                        "OPTIONS": "",
                        "DATA_TYPE": 0,
                        "TARGET_EXTENT": None,
                        "TARGET_EXTENT_CRS": None,
                        "MULTITHREADING": False,
                        "EXTRA": "",
                        "OUTPUT": FolderPath + "/MapSWAT/WGS84/LANDUSE.tif",
                    }
                    processing.run("gdal:warpreproject", params)

                    # Add Landuse to QGIS
                    fileName2 = FolderPath + "/MapSWAT/WGS84/LANDUSE.tif"
                    fileInfo = QFileInfo(fileName2)
                    baseName = fileInfo.baseName()
                    Landuse = QgsRasterLayer(fileName2, baseName)
                    QgsProject.instance().addMapLayer(Landuse)

                    self.pushButton_NewPolygon.setEnabled(True)
                    self.pushButton_OldPolygon.setEnabled(True)
                    self.pushButton_AddMaps.setEnabled(False)
                    self.pushButton_MERGE.setEnabled(False)

                except:
                    QMessageBox.warning(
                        None, "ADD LAYERS", "Please, select a raster layer in LANDUSE."
                    )

            self.progressBar.setValue(50)

        if self.checkBox_DEM.isChecked():
            fileName = self.mQgsFileWidget_DEM.filePath()
            rlayer = QgsRasterLayer(fileName, "DEM")
            crs_DEM = rlayer.crs()

            # Optimise map input process
            if crs_DEM == QgsCoordinateReferenceSystem("EPSG:4326"):
                # Add Landuse to QGIS
                rlayer = QgsRasterLayer(fileName, "DEM")
                QgsProject.instance().addMapLayer(rlayer)

                self.pushButton_NewPolygon.setEnabled(True)
                self.pushButton_OldPolygon.setEnabled(True)
                self.pushButton_AddMaps.setEnabled(False)
                self.pushButton_MERGE.setEnabled(False)

            else:
                try:
                    # Reproject DEM to WGS84
                    params = {
                        "INPUT": fileName,
                        "SOURCE_CRS": crs_DEM,
                        "TARGET_CRS": QgsCoordinateReferenceSystem("EPSG:4326"),
                        "RESAMPLING": 0,
                        "NODATA": None,
                        "TARGET_RESOLUTION": None,
                        "OPTIONS": "",
                        "DATA_TYPE": 0,
                        "TARGET_EXTENT": None,
                        "TARGET_EXTENT_CRS": None,
                        "MULTITHREADING": False,
                        "EXTRA": "",
                        "OUTPUT": FolderPath + "/MapSWAT/WGS84/DEM.tif",
                    }
                    processing.run("gdal:warpreproject", params)

                    # Add DEM to QGIS
                    fileName2 = FolderPath + "/MapSWAT/WGS84/DEM.tif"
                    fileInfo = QFileInfo(fileName2)
                    baseName = fileInfo.baseName()
                    DEM = QgsRasterLayer(fileName2, baseName)
                    QgsProject.instance().addMapLayer(DEM)

                    self.pushButton_NewPolygon.setEnabled(True)
                    self.pushButton_OldPolygon.setEnabled(True)
                    self.pushButton_AddMaps.setEnabled(False)
                    self.pushButton_MERGE.setEnabled(False)

                except:
                    QMessageBox.warning(
                        None, "ADD LAYERS", "Please, select a raster layer in DEM."
                    )

            self.progressBar.setValue(60)

        if self.lineX.isModified() and self.lineY.isModified():

            self.pushButton_Extension.setEnabled(True)

            # Create OUTLET
            crs_Outlet = self.mQgsProjection_Outlet.crs()
            writer = QgsVectorFileWriter(
                FolderPath + r"/MapSWAT/WGS84/OUTLET.shp",
                "UTF-8",
                QgsFields(),
                QgsWkbTypes.Point,
                crs_Outlet,
                "ESRI Shapefile",
            )

            # Add geometry - Draw point
            X = self.lineX.text()
            Y = self.lineY.text()
            fet = QgsFeature()
            fet.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(float(X), float(Y))))
            fet.setAttributes([1, "ID"])
            writer.addFeature(fet)
            del writer

            # Reproject OUTLET to WGS84
            params = {
                "INPUT": FolderPath + "/MapSWAT/WGS84/OUTLET.shp",
                "TARGET_CRS": QgsCoordinateReferenceSystem("EPSG:4326"),
                "OUTPUT": FolderPath + "/MapSWAT/WGS84/OUTLET_WGS84.shp",
            }
            processing.run("native:reprojectlayer", params)

            # Add OUTLET to QGIS
            layer = QgsVectorLayer(
                FolderPath + r"/MapSWAT/WGS84/OUTLET_WGS84.shp", "OUTLET", "ogr"
            )
            QgsProject.instance().addMapLayer(layer)

            # Activate layer and zoom
            layer1 = QgsProject.instance().mapLayersByName("OUTLET")[0]
            self.iface.setActiveLayer(layer1)
            self.iface.zoomToActiveLayer()
            self.canvas.refresh()

            self.progressBar.setValue(80)

        self.progressBar.setValue(100)
        self.progressBar.setValue(0)

    def merge(self):
        FolderPath = self.labelPath.text()

        # Select multiple QFileDialog files
        selectedFiles = QtWidgets.QFileDialog.getOpenFileNames(
            self, "Select files to merge", "", "TIFF files (*.tif)"
        )
        filenames = selectedFiles[0]

        self.progressBar.setValue(50)

        # Process for merging layers
        params = {
            "INPUT": filenames,
            "PCT": False,
            "SEPARATE": False,
            "NODATA_INPUT": None,
            "NODATA_OUTPUT": None,
            "OPTIONS": "",
            "EXTRA": "",
            "DATA_TYPE": 5,
            "OUTPUT": FolderPath
            + "\MapSWAT\SWAT_INPUT_MAPS\INFO_GIS\MERGE\DEM_merge.tif",
        }

        processing.run("gdal:merge", params)

        if os.path.isfile(
            FolderPath + "\MapSWAT\SWAT_INPUT_MAPS\INFO_GIS\MERGE\DEM_merge.tif"
        ):
            # Copy path in FileWidget_DEM
            self.mQgsFileWidget_DEM.setFilePath(
                FolderPath + "\MapSWAT\SWAT_INPUT_MAPS\INFO_GIS\MERGE\DEM_merge.tif"
            )

            self.checkBox_DEM.setChecked(True)
            self.progressBar.setValue(100)
            QMessageBox.information(None, "Merge DEMs", "Process completed.")
            self.pushButton_MERGE.setEnabled(False)

        else:
            QMessageBox.warning(None, "Merge DEMs", "Process not completed.")

        self.progressBar.setValue(100)
        self.progressBar.setValue(0)

    def Clip_New(self):
        FolderPath = self.labelPath.text()

        self.pushButton_NewPolygon.setEnabled(False)
        self.pushButton_OldPolygon.setEnabled(False)
        self.pushButton_Extension.setEnabled(False)
        self.pushButton_SWATinputs.setEnabled(True)

        # Create new polygon layer
        rectangle = QgsVectorFileWriter(
            FolderPath + "/MapSWAT/WGS84/POLYGON.shp",
            "UTF-8",
            QgsFields(),
            QgsWkbTypes.Polygon,
            QgsCoordinateReferenceSystem("EPSG:4326"),
            "ESRI Shapefile",
        )

        # Allow polygon layer editing
        fet = QgsFeature()
        rectangle.addFeature(fet)
        del rectangle

        # Add layer
        layer = QgsVectorLayer(
            FolderPath + "/MapSWAT/WGS84/POLYGON.shp", "POLYGON", "ogr"
        )
        QgsProject.instance().addMapLayer(layer)

        # Activate layer to edit
        layer1 = QgsProject.instance().mapLayersByName("POLYGON")[0]
        self.iface.setActiveLayer(layer1)

        # Open editor, delete first row and activate draw polygon
        layer = self.iface.activeLayer()
        layer.startEditing()
        layer.deleteFeature(0)
        self.iface.actionAddFeature().trigger()

        # Deactivate plugin
        self.hide()

        # Editor lock function, activated after attribute creation
        def feature_added():
            # Disconnect from the signal
            layer.featureAdded.disconnect()

            # Save changes and end edit mode
            layer.commitChanges()

            # Activate plugin
            self.show()

            # Copy layer POLYGON Input Maps folder
            layer.selectAll()
            params = {
                "INPUT": layer,
                "OUTPUT": FolderPath
                + "/MapSWAT/SWAT_INPUT_MAPS/INFO_GIS/POLYGON/POLYGON_WGS84.shp",
            }
            processing.run("native:saveselectedfeatures", params)
            layer.removeSelection()

        # Connect edit mode to closing function
        layer.featureAdded.connect(feature_added)

    def Clip_Old(self):
        FolderPath = self.labelPath.text()

        try:
            Old = self.mQgsFileWidget_Polygon.filePath()

            # Fix geometry of shapefile
            params = {
                "INPUT": Old,
                "METHOD": 1,
                "OUTPUT": FolderPath + "/MapSWAT/WGS84/POLYGON_fix.shp",
            }
            processing.run("native:fixgeometries", params)

            # Merge attribute table
            params = {
                "INPUT": FolderPath + "/MapSWAT/WGS84/POLYGON_fix.shp",
                "FIELD": [],
                "SEPARATE_DISJOINT": False,
                "OUTPUT": FolderPath + "/MapSWAT/WGS84/POLYGON_diss.shp",
            }
            processing.run("native:dissolve", params)

            # Reproject Polygon to WGS84
            params = {
                "INPUT": FolderPath + "/MapSWAT/WGS84/POLYGON_diss.shp",
                "TARGET_CRS": QgsCoordinateReferenceSystem("EPSG:4326"),
                "OUTPUT": FolderPath + "/MapSWAT/WGS84/POLYGON.shp",
            }
            processing.run("native:reprojectlayer", params)

            # Añadir Polygon Old a QGIS
            layer = QgsVectorLayer(
                FolderPath + "/MapSWAT/WGS84/POLYGON.shp", "POLYGON", "ogr"
            )
            QgsProject.instance().addMapLayer(layer)

            self.pushButton_NewPolygon.setEnabled(False)
            self.pushButton_OldPolygon.setEnabled(False)
            self.pushButton_Extension.setEnabled(False)
            self.pushButton_SWATinputs.setEnabled(True)

        except:
            QMessageBox.warning(None, "SHAPEFILE CLIP", "Please, select a shapefile.")

    def Clip_Extension(self):
        FolderPath = self.labelPath.text()

        self.pushButton_NewPolygon.setEnabled(False)
        self.pushButton_OldPolygon.setEnabled(False)
        self.pushButton_Extension.setEnabled(False)
        self.pushButton_SWATinputs.setEnabled(True)

        buffer = float(self.lineBuffer.text()) * 1000

        # Create buffer from OUTLET
        params = {
            "INPUT": FolderPath + "/MapSWAT/WGS84/OUTLET.shp",
            "DISTANCE": buffer,
            "SEGMENTS": 5,
            "END_CAP_STYLE": 2,
            "JOIN_STYLE": 0,
            "MITER_LIMIT": 2,
            "DISSOLVE": False,
            "OUTPUT": FolderPath
            + "/MapSWAT/SWAT_INPUT_MAPS/INFO_GIS/POLYGON/POLYGON_buffer.shp",
        }
        processing.run("native:buffer", params)

        # Reproject buffer to WGS84
        params2 = {
            "INPUT": FolderPath
            + "/MapSWAT/SWAT_INPUT_MAPS/INFO_GIS/POLYGON/POLYGON_buffer.shp",
            "TARGET_CRS": QgsCoordinateReferenceSystem("EPSG:4326"),
            "OUTPUT": FolderPath + "/MapSWAT/WGS84/POLYGON.shp",
        }
        processing.run("native:reprojectlayer", params2)

        # Add WGS84 buffer to QGIS
        layer = QgsVectorLayer(
            FolderPath + "/MapSWAT/WGS84/POLYGON.shp", "Buffer POLYGON", "ogr"
        )
        QgsProject.instance().addMapLayer(layer)

    def CREATE_INPUTS(self):
        FolderPath = self.labelPath.text()

        crs_target = self.mQgsProjection_Target.crs()

        # Check if selected CRS is valid
        if not crs_target.isValid():
            QMessageBox.warning(
                None,
                "CRS selection",
                "Please, select a valid CRS for SWAT/SWAT+ input maps",
            )
            return

        # Change the CRS of the project to crs_target
        QgsProject.instance().setCrs(crs_target)

        # Remove layers from the CANVAS
        QgsProject.instance().removeAllMapLayers()
        self.canvas.refresh()

        self.progressBar.setValue(10)

        if self.checkBox_Soil.isChecked():
            fileName = self.mQgsFileWidget_Soil.filePath()
            rlayer = QgsRasterLayer(fileName, "SOIL")
            crs_Soil = rlayer.crs()

            if crs_Soil == QgsCoordinateReferenceSystem("EPSG:4326"):
                # Clip the SOIL using the Polygon in WGS84
                params = {
                    "INPUT": fileName,
                    "MASK": FolderPath + "/MapSWAT/WGS84/POLYGON.shp",
                    "NODATA": None,
                    "ALPHA_BAND": False,
                    "CROP_TO_CUTLINE": True,
                    "KEEP_RESOLUTION": False,
                    "OPTIONS": "",
                    "DATA_TYPE": 0,
                    "OUTPUT": FolderPath + "/MapSWAT/WGS84/CLIPPED/SOIL.tif",
                }
                processing.run("gdal:cliprasterbymasklayer", params)

            else:
                # Clip the SOIL using the Polygon in WGS84
                params = {
                    "INPUT": FolderPath + "/MapSWAT/WGS84/SOIL.tif",
                    "MASK": FolderPath + "/MapSWAT/WGS84/POLYGON.shp",
                    "NODATA": None,
                    "ALPHA_BAND": False,
                    "CROP_TO_CUTLINE": True,
                    "KEEP_RESOLUTION": False,
                    "OPTIONS": "",
                    "DATA_TYPE": 0,
                    "OUTPUT": FolderPath + "/MapSWAT/WGS84/CLIPPED/SOIL.tif",
                }
                processing.run("gdal:cliprasterbymasklayer", params)

            # Reproject SOIL to crs_target
            crs_target = self.mQgsProjection_Target.crs()
            params2 = {
                "INPUT": FolderPath + "/MapSWAT/WGS84/CLIPPED/SOIL.tif",
                "SOURCE_CRS": QgsCoordinateReferenceSystem("EPSG:4326"),
                "TARGET_CRS": crs_target,
                "RESAMPLING": 0,
                "NODATA": None,
                "TARGET_RESOLUTION": None,
                "OPTIONS": "",
                "DATA_TYPE": 0,
                "TARGET_EXTENT": None,
                "TARGET_EXTENT_CRS": None,
                "MULTITHREADING": False,
                "EXTRA": "",
                "OUTPUT": FolderPath + "\MapSWAT\SWAT_INPUT_MAPS\SOIL\SOIL.tif",
            }
            processing.run("gdal:warpreproject", params2)

            # Adding clipped and reprojected SOIL to QGIS
            fileName = FolderPath + "\MapSWAT\SWAT_INPUT_MAPS\SOIL\SOIL.tif"
            fileInfo = QFileInfo(fileName)
            baseName = fileInfo.baseName()
            SOIL = QgsRasterLayer(fileName, baseName)
            QgsProject.instance().addMapLayer(SOIL)

            # Zoom to layer
            zoom = SOIL.extent()
            self.canvas.setExtent(zoom)

            self.progressBar.setValue(30)

            # Obtain raster classes in the area
            params = {
                "INPUT_RASTER": FolderPath + "/MapSWAT/WGS84/CLIPPED/SOIL.tif",
                "RASTER_BAND": 1,
                "INPUT_VECTOR": FolderPath + "/MapSWAT/WGS84/POLYGON.shp",
                "COLUMN_PREFIX": "",
                "OUTPUT": FolderPath + "/MapSWAT/WGS84/SOIL_Values.shp",
            }

            processing.run("native:zonalhistogram", params)

            # Remove excess columns
            layer = QgsVectorLayer(
                FolderPath + "/MapSWAT/WGS84/SOIL_Values.shp", "SOIL_Values", "ogr"
            )
            caps = layer.dataProvider().capabilities()
            id1 = layer.fields().indexFromName("FID")
            layer.startEditing()
            layer.deleteAttribute(id1)
            layer.commitChanges()
            id2 = layer.fields().indexFromName("NODATA")
            layer.startEditing()
            layer.deleteAttribute(id2)
            layer.commitChanges()

            # Copy table header attributes
            field_names = [field.name() for field in layer.fields()]

            # Create CSV with raster layer data
            with open(
                FolderPath + "\MapSWAT\SWAT_INPUT_MAPS\SOIL\Soil_lookup.csv",
                "w",
                newline="",
            ) as csvfile:
                filewriter = csv.writer(csvfile)
                filewriter.writerow(["SOIL_ID", "SNAM"])
                filewriter.writerows(zip(field_names))
                csvfile.close()

        if self.checkBox_Landuse.isChecked():
            fileName = self.mQgsFileWidget_Landuse.filePath()
            rlayer = QgsRasterLayer(fileName, "LANDUSE")
            crs_Landuse = rlayer.crs()

            if crs_Landuse == QgsCoordinateReferenceSystem("EPSG:4326"):
                # Clip the LANDUSE using the Polygon in WGS84
                params = {
                    "INPUT": fileName,
                    "MASK": FolderPath + "/MapSWAT/WGS84/POLYGON.shp",
                    "NODATA": None,
                    "ALPHA_BAND": False,
                    "CROP_TO_CUTLINE": True,
                    "KEEP_RESOLUTION": False,
                    "OPTIONS": "",
                    "DATA_TYPE": 0,
                    "OUTPUT": FolderPath + "/MapSWAT/WGS84/CLIPPED/LANDUSE.tif",
                }
                processing.run("gdal:cliprasterbymasklayer", params)

            else:
                # Clip the LANDUSE using the Polygon in WGS84
                params = {
                    "INPUT": FolderPath + "/MapSWAT/WGS84/LANDUSE.tif",
                    "MASK": FolderPath + "/MapSWAT/WGS84/POLYGON.shp",
                    "NODATA": None,
                    "ALPHA_BAND": False,
                    "CROP_TO_CUTLINE": True,
                    "KEEP_RESOLUTION": False,
                    "OPTIONS": "",
                    "DATA_TYPE": 0,
                    "OUTPUT": FolderPath + "/MapSWAT/WGS84/CLIPPED/LANDUSE.tif",
                }
                processing.run("gdal:cliprasterbymasklayer", params)

            # Reproject LANDUSE to crs_target
            crs_target = self.mQgsProjection_Target.crs()
            params2 = {
                "INPUT": FolderPath + "/MapSWAT/WGS84/CLIPPED/LANDUSE.tif",
                "SOURCE_CRS": QgsCoordinateReferenceSystem("EPSG:4326"),
                "TARGET_CRS": crs_target,
                "RESAMPLING": 0,
                "NODATA": None,
                "TARGET_RESOLUTION": None,
                "OPTIONS": "",
                "DATA_TYPE": 0,
                "TARGET_EXTENT": None,
                "TARGET_EXTENT_CRS": None,
                "MULTITHREADING": False,
                "EXTRA": "",
                "OUTPUT": FolderPath + "\MapSWAT\SWAT_INPUT_MAPS\LANDUSE\LANDUSE.tif",
            }
            processing.run("gdal:warpreproject", params2)

            # Adding clipped and reprojected LANDUSE to QGIS
            fileName = FolderPath + "\MapSWAT\SWAT_INPUT_MAPS\LANDUSE\LANDUSE.tif"
            fileInfo = QFileInfo(fileName)
            baseName = fileInfo.baseName()
            LANDUSE = QgsRasterLayer(fileName, baseName)
            QgsProject.instance().addMapLayer(LANDUSE)

            # Zoom to layer
            zoom = LANDUSE.extent()
            self.canvas.setExtent(zoom)

            self.progressBar.setValue(50)

            # Obtain raster classes in the area
            params = {
                "INPUT_RASTER": FolderPath + "/MapSWAT/WGS84/CLIPPED/LANDUSE.tif",
                "RASTER_BAND": 1,
                "INPUT_VECTOR": FolderPath + "/MapSWAT/WGS84/POLYGON.shp",
                "COLUMN_PREFIX": "",
                "OUTPUT": FolderPath + "/MapSWAT/WGS84/LANDUSE_Values.shp",
            }
            processing.run("native:zonalhistogram", params)

            # Remove excess columns
            layer = QgsVectorLayer(
                FolderPath + "/MapSWAT/WGS84/LANDUSE_Values.shp",
                "LANDUSE_Values",
                "ogr",
            )
            caps = layer.dataProvider().capabilities()
            id1 = layer.fields().indexFromName("FID")
            layer.startEditing()
            layer.deleteAttribute(id1)
            layer.commitChanges()
            id2 = layer.fields().indexFromName("NODATA")
            layer.startEditing()
            layer.deleteAttribute(id2)
            layer.commitChanges()

            # Copy table header attributes
            field_names = [field.name() for field in layer.fields()]

            # Create CSV with raster layer data
            with open(
                FolderPath + "\MapSWAT\SWAT_INPUT_MAPS\LANDUSE\Landuse_lookup.csv",
                "w",
                newline="",
            ) as csvfile:
                filewriter = csv.writer(csvfile)
                filewriter.writerow(["LANDUSE_ID", "SWAT_CODE"])
                filewriter.writerows(zip(field_names))
                csvfile.close()

        if self.checkBox_DEM.isChecked():
            fileName = self.mQgsFileWidget_DEM.filePath()
            rlayer = QgsRasterLayer(fileName, "DEM")
            crs_DEM = rlayer.crs()

            # Optimise map input process
            if crs_DEM == QgsCoordinateReferenceSystem("EPSG:4326"):
                # Clipping the DEM using the Polygon in WGS84
                params = {
                    "INPUT": fileName,
                    "MASK": FolderPath + "/MapSWAT/WGS84/POLYGON.shp",
                    "NODATA": None,
                    "ALPHA_BAND": False,
                    "CROP_TO_CUTLINE": True,
                    "KEEP_RESOLUTION": False,
                    "OPTIONS": "",
                    "DATA_TYPE": 0,
                    "OUTPUT": FolderPath + "/MapSWAT/WGS84/CLIPPED/DEM.tif",
                }
                processing.run("gdal:cliprasterbymasklayer", params)

            else:
                # Clipping the DEM using the Polygon in WGS84
                params = {
                    "INPUT": FolderPath + "/MapSWAT/WGS84/DEM.tif",
                    "MASK": FolderPath + "/MapSWAT/WGS84/POLYGON.shp",
                    "NODATA": None,
                    "ALPHA_BAND": False,
                    "CROP_TO_CUTLINE": True,
                    "KEEP_RESOLUTION": False,
                    "OPTIONS": "",
                    "DATA_TYPE": 0,
                    "OUTPUT": FolderPath + "/MapSWAT/WGS84/CLIPPED/DEM.tif",
                }
                processing.run("gdal:cliprasterbymasklayer", params)

            # Reproject DEM to crs_target
            crs_target = self.mQgsProjection_Target.crs()
            params2 = {
                "INPUT": FolderPath + "/MapSWAT/WGS84/CLIPPED/DEM.tif",
                "SOURCE_CRS": QgsCoordinateReferenceSystem("EPSG:4326"),
                "TARGET_CRS": crs_target,
                "RESAMPLING": 0,
                "NODATA": None,
                "TARGET_RESOLUTION": None,
                "OPTIONS": "",
                "DATA_TYPE": 0,
                "TARGET_EXTENT": None,
                "TARGET_EXTENT_CRS": None,
                "MULTITHREADING": False,
                "EXTRA": "",
                "OUTPUT": FolderPath + "\MapSWAT\SWAT_INPUT_MAPS\DEM\DEM.tif",
            }
            processing.run("gdal:warpreproject", params2)

            # Adding clipped and reprojected DEM to QGIS
            fileName = FolderPath + "\MapSWAT\SWAT_INPUT_MAPS\DEM\DEM.tif"
            fileInfo = QFileInfo(fileName)
            baseName = fileInfo.baseName()
            DEM = QgsRasterLayer(fileName, baseName)
            QgsProject.instance().addMapLayer(DEM)

            # Zoom to layer
            zoom = DEM.extent()
            self.canvas.setExtent(zoom)

            self.progressBar.setValue(60)

        if self.lineX.isModified() and self.lineY.isModified():
            # Reproject OUTLET to crs_target
            params3 = {
                "INPUT": FolderPath + "/MapSWAT/WGS84/OUTLET_WGS84.shp",
                "TARGET_CRS": crs_target,
                "OUTPUT": FolderPath
                + "\MapSWAT\SWAT_INPUT_MAPS\INFO_GIS\OUTLET\OUTLET.shp",
            }
            processing.run("native:reprojectlayer", params3)

            # Adding OUTLET reprojected to QGIS
            layer = QgsVectorLayer(
                FolderPath + "\MapSWAT\SWAT_INPUT_MAPS\INFO_GIS\OUTLET\OUTLET.shp",
                "OUTLET",
                "ogr",
            )
            QgsProject.instance().addMapLayer(layer)

            self.progressBar.setValue(80)

        self.progressBar.setValue(90)
        self.progressBar.setValue(0)

        # Deactivate plugin
        self.showMinimized()

        # Message Process completed
        text = "Process completed successfully."
        msgINFO = QMessageBox()
        msgINFO.setWindowIcon(QIcon(":/imgMapSWAT/images/icon.png"))
        msgINFO.setWindowTitle("MapSWAT")
        msgINFO.setText(text)
        msgINFO.setStandardButtons(QMessageBox.Ok)
        msgINFO.exec_()

    def Open(self):
        FolderPath = self.labelPath.text()
        webbrowser.open(FolderPath + "\MapSWAT\SWAT_INPUT_MAPS")

    def Close(self):
        reply = QMessageBox.question(
            None,
            "Warning",
            "When you close MapSWAT the QGIS canvas will be cleared.\n\nWould you like to continue?",
            QMessageBox.Yes,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:

            # Remove layers from the CANVAS
            QgsProject.instance().removeAllMapLayers()
            self.canvas.refresh()

            # Close plugin
            self.close()
        else:
            pass

    def info(self):
        text = "<b>MapSWAT</b> is a QGIS plugin for preparing SWAT or SWAT+ input maps.<br><br><b>User manual</b>: https://adrlballesteros.github.io/MapSWAT/ <br><br><b>Research paper</b>: https://doi.org/10.1016/j.envsoft.2024.106108 <br><br>If you have feedback or suggestions, please contact me at <b>alopez6@ucam.edu</b>. <br><br>If you find this plugin useful, or if it has saved you time in your work, consider supporting it by inviting me for a coffee. Thanks 😊"
        msgINFO = QMessageBox()
        msgINFO.setWindowIcon(QIcon(":/imgMapSWAT/images/icon.png"))
        msgINFO.setWindowTitle("Help & About")
        msgINFO.setText(text)
        msgINFO.setTextFormat(Qt.RichText)
        msgINFO.setStandardButtons(QMessageBox.Ok)
        msgINFO.exec_()

    def coffee(self):
        self.labelCheck_coffee.setText("😊")
        url = "https://www.buymeacoffee.com/alopez6"
        webbrowser.open(url)
