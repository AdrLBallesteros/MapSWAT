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

from MapSWAT_v3.gui.generated.ui_dialog_GEE import Ui_BaseDialog_GEE

from qgis.gui import QgsMapToolEmitPoint
from qgis.core import QgsProject, QgsRasterLayer
from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry
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
)

import os.path
import os
import shutil
import processing
import requests
import zipfile
import csv
import webbrowser
import json


class BaseDialog_GEE(QDialog, Ui_BaseDialog_GEE):

    def __init__(self, iface):
        QDialog.__init__(self)
        self.setupUi(self)
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self.plugin_dir = os.path.dirname(os.path.abspath(__file__))

        self.polygon = None

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

        # Filter in QGSFileWidget
        self.mQgsFileWidget_Polygon.setFilter("Shapefiles (*.shp)")

        # Activate button lock
        self.pushButton_MANUAL.setEnabled(False)
        self.pushButton_SHAPEFILE.setEnabled(False)
        self.pushButton_BUFFER.setEnabled(False)
        self.pushButton_AUTOBASIN.setEnabled(False)
        self.pushButton_SWATinputs.setEnabled(False)
        self.pushButton_GetMaps.setEnabled(False)

        # Change the CRS of the project to WGS84
        WGS84 = QgsCoordinateReferenceSystem(3857)
        QgsProject.instance().setCrs(WGS84)

        # Get the GEE cloud project ID and ee.Initialize(project='my-project')
        plugin_path = os.path.abspath(__file__)
        plugin_directory = os.path.dirname(plugin_path)
        GEE_project_file = os.path.join(
            plugin_directory, "resources", "GEE_project_ID.json"
        )
        if os.path.exists(GEE_project_file):
            with open(GEE_project_file, "r") as file:
                GEE_ID = json.load(file)

        import ee
        from ee_plugin import Map

        ee.Initialize(project=GEE_ID[0])  # Needed in the last version of GEE

        # Connect to GEE
        test = ee.String(
            "<b>*Successfully connected to Google Earth Engine (GEE)*</b>"
        ).getInfo()
        msg1 = QMessageBox()
        msg1.setWindowIcon(QIcon(":/imgMapSWAT/images/icon.png"))
        msg1.setIconPixmap(QtGui.QPixmap(":/imgMapSWAT/images/ee.png"))
        msg1.setWindowTitle("MapSWAT GEE")
        msg1.setText('<div align="center">' + test + "</div>")
        msg1.setStandardButtons(QMessageBox.Ok)
        msg1.exec_()

    def InitialWindow(self):
        self.show()
        # Code to create a window to get the path of the MapSWAT project
        msg = QMessageBox()
        msg.setWindowIcon(QIcon(":/imgMapSWAT/images/icon.png"))
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
                path13 = folder + "\MapSWAT\SWAT_INPUT_MAPS\GWFLOW"
                os.makedirs(path13, exist_ok=True)
            except:
                self.close()
        else:
            self.close()

    def AddOutlet(self):
        import ee
        from ee_plugin import Map

        FolderPath = self.labelPath.text()

        if self.lineX.isModified() and self.lineY.isModified():
            try:
                self.pushButton_AddBasemap.setEnabled(False)
                self.pushButton_point.setEnabled(False)

                # Create  OUTLET
                X = self.lineX.text()
                Y = self.lineY.text()
                crs_Outlet = self.mQgsProjection_Outlet.crs()

                # Extract CRS id
                crs_id = crs_Outlet.authid()
                id = str(crs_id)

                # Add ee.Geometry.Point to QGIS canvas
                point = ee.Geometry.Point([float(X), float(Y)], str(crs_id))

                self.progressBar.setValue(50)

                # Add basemap to QGIS canvas
                basemap_url = (
                    "type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png&zmax=19&zmin=0&crs="
                    + crs_id
                )
                basemap = QgsRasterLayer(basemap_url, "Basemap", "wms")
                QgsProject.instance().addMapLayer(basemap)

                # Add GEE point to canvas
                try:
                    Map.addLayer(point, {"color": "red", "width": 5}, "Outlet")
                except:
                    pass

                Map.centerObject(point, 10)

                # Create a point shapefile from coordinates
                crs_Outlet = self.mQgsProjection_Outlet.crs()
                writer = QgsVectorFileWriter(
                    FolderPath + "/MapSWAT/WGS84/OUTLET.shp",
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

            # Exception - Reboot buttons and basemap
            except:
                self.progressBar.setValue(0)
                self.pushButton_AddBasemap.setEnabled(True)
                self.pushButton_point.setEnabled(True)

                layers = QgsProject.instance().mapLayersByName("Basemap")
                for layer in layers:
                    QgsProject.instance().removeMapLayer(layer.id())
                self.canvas.refresh()

                QMessageBox.warning(
                    None,
                    "Coordinates error",
                    "Please, check the outlet coordinates and selected CRS.",
                )

            self.progressBar.setValue(80)

        else:
            QMessageBox.information(
                None,
                "Outlet coordinates not found",
                "Please, add the outlet coordinates in the X, Y boxes.",
            )

        self.progressBar.setValue(100)
        self.progressBar.setValue(0)
        self.pushButton_GetMaps.setEnabled(True)

    def AddBasemap(self):
        self.pushButton_point.setEnabled(False)
        self.pushButton_AddBasemap.setEnabled(False)
        self.pushButton_GetMaps.setEnabled(True)

        basemap_url = "type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png&zmax=19&zmin=0&crs=EPSG3857"
        basemap = QgsRasterLayer(basemap_url, "Basemap", "wms")
        QgsProject.instance().addMapLayer(basemap)

        extent = basemap.extent()
        self.canvas.setExtent(extent)
        self.canvas.refresh()

    def GetMaps(self):
        if self.lineX.isModified() and self.lineY.isModified():
            self.pushButton_BUFFER.setEnabled(True)
            self.pushButton_AUTOBASIN.setEnabled(True)

        if self.checkBox_DEM.isChecked():
            self.pushButton_MANUAL.setEnabled(True)
            self.pushButton_SHAPEFILE.setEnabled(True)
            self.comboBox_DEM.setEnabled(False)
            self.checkBox_DEM.setEnabled(False)

        if self.checkBox_Landuse.isChecked():
            self.pushButton_MANUAL.setEnabled(True)
            self.pushButton_SHAPEFILE.setEnabled(True)
            self.comboBox_LANDUSE.setEnabled(False)
            self.checkBox_Landuse.setEnabled(False)

        if self.checkBox_Soil.isChecked():
            self.pushButton_MANUAL.setEnabled(True)
            self.pushButton_SHAPEFILE.setEnabled(True)
            self.comboBox_SOIL.setEnabled(False)
            self.checkBox_Soil.setEnabled(False)

        if self.checkBox_GWFLOW.isChecked():
            self.pushButton_MANUAL.setEnabled(True)
            self.pushButton_SHAPEFILE.setEnabled(True)
            self.checkBox_GWFLOW.setEnabled(False)

        self.progressBar.setValue(100)
        self.progressBar.setValue(0)

    def Clip_New(self):
        FolderPath = self.labelPath.text()

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

            # Activar plugin
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

            self.progressBar.setValue(50)

            self.GEE_Mask()

        # Connect Editor mode to closing function
        layer.featureAdded.connect(feature_added)

    def GEE_Mask(self):
        import ee
        from ee_plugin import Map

        self.pushButton_MANUAL.setEnabled(False)
        self.pushButton_SHAPEFILE.setEnabled(False)
        self.pushButton_BUFFER.setEnabled(False)
        self.pushButton_AUTOBASIN.setEnabled(False)

        FolderPath = self.labelPath.text()
        layer = QgsVectorLayer(
            FolderPath + "/MapSWAT/WGS84/POLYGON.shp", "POLYGON", "ogr"
        )

        # Get polygon coordinates
        for feature in layer.getFeatures():
            # Get the geometry of the feature
            geom = feature.geometry()
            # QMessageBox.information(None, "Polygon", str(geom))
            if geom.type() == QgsWkbTypes.PolygonGeometry:
                multiPolygon = geom.asMultiPolygon()
                # QMessageBox.information(None, "Polygon", str(multiPolygon))
                for polygon in multiPolygon:
                    for ring in polygon:
                        listCoords = []
                        for point in ring:
                            coords = [point.x(), point.y()]
                            listCoords.append(coords)
                        # QMessageBox.information(None, "Polygon", str(list))

        # Transform shapefile to GEE polygon from coordinates
        self.polygon = ee.Geometry.Polygon([listCoords])

        # Add GEE layer to Map
        try:
            Map.addLayer(self.polygon, {"color": "black"}, "GEE Mask Layer")
        except:
            pass

        Map.centerObject(self.polygon, 10)

        self.progressBar.setValue(100)
        self.progressBar.setValue(0)

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

            # Adding Polygon Old to QGIS
            layer = QgsVectorLayer(
                FolderPath + "/MapSWAT/WGS84/POLYGON.shp", "POLYGON", "ogr"
            )
            QgsProject.instance().addMapLayer(layer)

            self.GEE_Mask()

            self.pushButton_SWATinputs.setEnabled(True)

        except:
            QMessageBox.warning(
                None, "SHAPEFILE CLIP", "Please, select a shapefile layer."
            )

    def Clip_Extension(self):
        import ee
        from ee_plugin import Map

        FolderPath = self.labelPath.text()

        if QgsProject.instance().mapLayersByName("GEE Mask Layer"):
            # Select layer
            buffer = QgsProject.instance().mapLayersByName("GEE Mask Layer")[0]
            # Remove layer from canvas
            QgsProject.instance().removeMapLayer(buffer.id())

        self.pushButton_MANUAL.setEnabled(False)
        self.pushButton_SHAPEFILE.setEnabled(False)
        # self.pushButton_BUFFER.setEnabled(False)
        # self.pushButton_AUTOBASIN.setEnabled(False)
        self.pushButton_SWATinputs.setEnabled(True)

        buffer = float(self.lineBuffer.text()) * 1000

        # Add OUTLET to QGIS
        layer = QgsVectorLayer(
            FolderPath + r"/MapSWAT/WGS84/OUTLET_WGS84.shp", "OUTLET", "ogr"
        )

        for feature in layer.getFeatures():
            # Get the geometry of the feature
            geom = feature.geometry()
            if geom.type() == QgsWkbTypes.PointGeometry:
                pointCoords = geom.asPoint()
                coords = [pointCoords.x(), pointCoords.y()]
                # QMessageBox.information(None, "Polygon", str(coords))

        point = ee.Geometry.Point(coords)
        bufferedPoint = point.buffer(buffer)

        self.polygon = bufferedPoint

        # Add GEE layer to Map
        try:
            Map.addLayer(bufferedPoint, {"color": "black"}, "GEE Mask Layer")
        except:
            pass
        Map.centerObject(bufferedPoint, 10)

    def Clip_Autobasin(self):
        import ee
        from ee_plugin import Map

        FolderPath = self.labelPath.text()

        if QgsProject.instance().mapLayersByName("GEE Mask Layer"):
            # Select layer
            Autobasin = QgsProject.instance().mapLayersByName("GEE Mask Layer")[0]
            # Remove layer from canvas
            QgsProject.instance().removeMapLayer(Autobasin.id())

        self.pushButton_MANUAL.setEnabled(False)
        self.pushButton_SHAPEFILE.setEnabled(False)
        # self.pushButton_BUFFER.setEnabled(False)
        self.pushButton_SWATinputs.setEnabled(True)

        T = self.comboBox_AUTOBASIN.currentText()
        if T == "HydroSHEDS Basins L-7":
            basin = ee.FeatureCollection("WWF/HydroSHEDS/v1/Basins/hybas_7")
        elif T == "HydroSHEDS Basins L-8":
            basin = ee.FeatureCollection("WWF/HydroSHEDS/v1/Basins/hybas_8")
        elif T == "HydroSHEDS Basins L-9":
            basin = ee.FeatureCollection("WWF/HydroSHEDS/v1/Basins/hybas_9")
        elif T == "HydroSHEDS Basins L-10":
            basin = ee.FeatureCollection("WWF/HydroSHEDS/v1/Basins/hybas_10")
        elif T == "HydroSHEDS Basins L-11":
            basin = ee.FeatureCollection("WWF/HydroSHEDS/v1/Basins/hybas_11")
        elif T == "HydroSHEDS Basins L-12":
            basin = ee.FeatureCollection("WWF/HydroSHEDS/v1/Basins/hybas_12")

        # Add OUTLET to QGIS
        layer = QgsVectorLayer(
            FolderPath + r"/MapSWAT/WGS84/OUTLET_WGS84.shp", "OUTLET", "ogr"
        )
        for feature in layer.getFeatures():
            # Get the geometry of the feature
            geom = feature.geometry()
            if geom.type() == QgsWkbTypes.PointGeometry:
                pointCoords = geom.asPoint()
                coords = [pointCoords.x(), pointCoords.y()]
                # QMessageBox.information(None, "Polygon", str(coords))
        point = ee.Geometry.Point(coords)
        selectedBasin = basin.filterBounds(point)

        self.polygon = selectedBasin

        try:
            Map.addLayer(selectedBasin, {"color": "black"}, "GEE Mask Layer")
        except:
            pass

        Map.centerObject(point, 10)

    def CREATE_INPUTS(self):
        import ee
        from ee_plugin import Map

        FolderPath = self.labelPath.text()

        crs_target = self.mQgsProjection_Target.crs()
        crs_target_id = str(crs_target.authid())

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

        if self.checkBox_Landuse.isChecked():
            LULCpath = FolderPath + "\MapSWAT\SWAT_INPUT_MAPS\LANDUSE"

            LULCfile = self.comboBox_LANDUSE.currentText()

            if LULCfile == "Copernicus Global Land Cover 2019":
                LULC = ee.Image(
                    "COPERNICUS/Landcover/100m/Proba-V-C3/Global/2019"
                ).select("discrete_classification")
                resolution = 100
                resolution_ini = 100
                json_path = os.path.join(
                    self.plugin_dir, "resources/LULC_Copernicus.json"
                )

            if LULCfile == "GlobCover: Global Land Cover Map 2009":
                LULC = ee.Image("ESA/GLOBCOVER_L4_200901_200912_V2_3").select(
                    "landcover"
                )
                resolution = 300
                resolution_ini = 300
                json_path = os.path.join(
                    self.plugin_dir, "resources/LULC_GlobCover.json"
                )

            if LULCfile == "Copernicus CORINE Land Cover 1990 (only Europe)":
                LULC = ee.Image("COPERNICUS/CORINE/V20/100m/1990").select("landcover")
                resolution = 100
                resolution_ini = 100
                json_path = os.path.join(self.plugin_dir, "resources/LULC_CORINE.json")

            if LULCfile == "Copernicus CORINE Land Cover 2000 (only Europe)":
                LULC = ee.Image("COPERNICUS/CORINE/V20/100m/2000").select("landcover")
                resolution = 100
                resolution_ini = 100
                json_path = os.path.join(self.plugin_dir, "resources/LULC_CORINE.json")

            if LULCfile == "Copernicus CORINE Land Cover 2006 (only Europe)":
                LULC = ee.Image("COPERNICUS/CORINE/V20/100m/2006").select("landcover")
                resolution = 100
                resolution_ini = 100
                json_path = os.path.join(self.plugin_dir, "resources/LULC_CORINE.json")

            if LULCfile == "Copernicus CORINE Land Cover 2012 (only Europe)":
                LULC = ee.Image("COPERNICUS/CORINE/V20/100m/2012").select("landcover")
                resolution = 100
                resolution_ini = 100
                json_path = os.path.join(self.plugin_dir, "resources/LULC_CORINE.json")

            if LULCfile == "Copernicus CORINE Land Cover 2018 (only Europe)":
                LULC = ee.Image("COPERNICUS/CORINE/V20/100m/2018").select("landcover")
                resolution = 100
                resolution_ini = 100
                json_path = os.path.join(self.plugin_dir, "resources/LULC_CORINE.json")

            # Check the type of GEE object, if Geometry == True
            if isinstance(self.polygon, ee.geometry.Geometry):
                i = 0
                while i < 100:
                    # For geometry
                    try:
                        url = LULC.getDownloadURL(
                            {
                                "name": "LULC",
                                "scale": resolution,
                                "crs": crs_target_id,
                                "region": self.polygon.getInfo(),
                                "fileFormat": "GeoTIFF",
                            }
                        )
                        if resolution > resolution_ini:
                            QMessageBox.information(
                                None,
                                "Map Resolution Adjustment",
                                f"GEE request exceeds the limit of 32 MB. Raster resolution adjusted to {resolution} meters.",
                            )
                        break
                    except ee.ee_exception.EEException:
                        resolution += 10
                        i += 1

            # Check the type of GEE object, if FeatureCollection == True
            elif isinstance(self.polygon, ee.FeatureCollection):
                i = 0
                while i < 100:
                    # For feature collection
                    try:
                        url = LULC.getDownloadURL(
                            {
                                "name": "LULC",
                                "scale": resolution,
                                "crs": crs_target_id,
                                "region": self.polygon.geometry().bounds().getInfo(),
                                "fileFormat": "GeoTIFF",
                            }
                        )
                        if resolution > resolution_ini:
                            QMessageBox.information(
                                None,
                                "Map Resolution Adjustment",
                                f"GEE request exceeds the limit of 32 MB. Raster resolution adjusted to {resolution} meters.",
                            )
                        break
                    except ee.ee_exception.EEException:
                        resolution += 10
                        i += 1

            # Open the URL and download the zip
            save_path = os.path.join(
                FolderPath, "MapSWAT/SWAT_INPUT_MAPS/LANDUSE/LANDUSE.zip"
            )
            response = requests.get(url)
            response.raise_for_status()
            with open(save_path, "wb") as f:
                f.write(response.content)

            # Extract the files of the zip file in the local folder
            dest_directory = os.path.dirname(save_path)
            with zipfile.ZipFile(save_path, "r") as zip_ref:
                zip_ref.extractall(dest_directory)

            # Select the tif file of the local folder
            files = os.listdir(dest_directory)
            for file in files:
                if file.endswith(".tif"):
                    fileName = os.path.join(dest_directory, file)

            # Add LULC in QGIS canvas
            fileInfo = QFileInfo(fileName)
            baseName = fileInfo.baseName()
            LULC = QgsRasterLayer(fileName, baseName)
            QgsProject.instance().addMapLayer(LULC)

            # Zoom to the layer
            zoom = LULC.extent()
            self.canvas.setExtent(zoom)
            self.canvas.refresh()

            self.progressBar.setValue(30)

            ##Create the lookup tables for SWAT
            provider = LULC.dataProvider()
            LULC_values = set()

            # Iterate over raster rows and columns. Extract unique values from raster
            for row in range(provider.xSize()):
                for col in range(provider.ySize()):
                    position = QgsPointXY(
                        LULC.extent().xMinimum() + LULC.rasterUnitsPerPixelX() * col,
                        LULC.extent().yMaximum() - LULC.rasterUnitsPerPixelY() * row,
                    )
                    value, result = provider.sample(position, 1)
                    if result:
                        LULC_values.add(int(value))

            # QMessageBox.information(None, "LULC URL", str(LULC_values))

            # Create the CSV file
            csv_path = (
                FolderPath + "\MapSWAT\SWAT_INPUT_MAPS\LANDUSE\Landuse_lookup.csv"
            )
            # json_path = os.path.join(self.plugin_dir, 'resources/LULC_GlobCover.json')
            LULC_sorted_values = sorted(LULC_values)

            ##Create the lookup tables for SWAT (continue)
            # Copy unique values from raster and paste in lookup table
            with open(csv_path, "w", newline="") as csvfile:
                filewriter = csv.writer(csvfile)
                filewriter.writerow(["LANDUSE_ID", "SWAT_CODE"])
                for value in LULC_sorted_values:
                    filewriter.writerow([value])

            # Read JSON file
            with open(json_path, "r") as json_file:
                json_data = json.load(json_file)
                value_to_landuse = {
                    item["Value"]: item["Landuse"] for item in json_data
                }

            # Read CSV file and paste values from CSV based on first column
            rows = []
            with open(csv_path, "r") as csv_file:
                reader = csv.DictReader(csv_file)

                for row in reader:
                    landuse_id = int(row["LANDUSE_ID"])
                    if landuse_id in value_to_landuse:
                        row["SWAT_CODE"] = value_to_landuse[landuse_id]
                    rows.append(row)
            with open(csv_path, "w", newline="") as csv_file:
                fieldnames = rows[0].keys()
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

        if self.checkBox_Soil.isChecked():
            SOILpath = FolderPath + "\MapSWAT\SWAT_INPUT_MAPS\SOIL"

            SOILfile = self.comboBox_SOIL.currentText()

            if SOILfile == "DSOLMap: Digital Soil Open Land Map":
                SOIL = ee.Image("projects/ee-alopez6/assets/DSOLMap")
                resolution = 250
                resolution_ini = 250
                json_path = os.path.join(self.plugin_dir, "resources/Soil_DSOLMap.json")

            # Check the type of GEE object, if Geometry == True
            if isinstance(self.polygon, ee.geometry.Geometry):
                i = 0
                while i < 100:
                    # For geometry
                    try:
                        url = SOIL.getDownloadURL(
                            {
                                "name": "SOIL",
                                "scale": resolution,
                                "crs": crs_target_id,
                                "region": self.polygon.getInfo(),
                                "fileFormat": "GeoTIFF",
                            }
                        )
                        if resolution > resolution_ini:
                            QMessageBox.information(
                                None,
                                "Map Resolution Adjustment",
                                f"GEE request exceeds the limit of 32 MB. Raster resolution adjusted to {resolution} meters.",
                            )
                        break

                    except ee.ee_exception.EEException:
                        resolution += 10
                        i += 1

            # Check the type of GEE object, if FeatureCollection == True
            elif isinstance(self.polygon, ee.FeatureCollection):
                i = 0
                while i < 100:
                    # For feature collection
                    try:
                        url = SOIL.getDownloadURL(
                            {
                                "name": "SOIL",
                                "scale": resolution,
                                "crs": crs_target_id,
                                "region": self.polygon.geometry().bounds().getInfo(),
                                "fileFormat": "GeoTIFF",
                            }
                        )
                        if resolution > resolution_ini:
                            QMessageBox.information(
                                None,
                                "Map Resolution Adjustment",
                                f"GEE request exceeds the limit of 32 MB. Raster resolution adjusted to {resolution} meters.",
                            )
                        break
                    except ee.ee_exception.EEException:
                        resolution += 10
                        i += 1

            # Open the URL and download the zip
            save_path = os.path.join(
                FolderPath, "MapSWAT/SWAT_INPUT_MAPS/SOIL/SOIL.zip"
            )
            response = requests.get(url)
            response.raise_for_status()
            with open(save_path, "wb") as f:
                f.write(response.content)

            # Extract the files of the zip file in the local folder
            dest_directory = os.path.dirname(save_path)
            with zipfile.ZipFile(save_path, "r") as zip_ref:
                zip_ref.extractall(dest_directory)

            # Select the tif file of the local folder
            files = os.listdir(dest_directory)
            for file in files:
                if file.endswith(".tif"):
                    fileName = os.path.join(dest_directory, file)

            # Add LULC in QGIS canvas
            fileInfo = QFileInfo(fileName)
            baseName = fileInfo.baseName()
            SOIL = QgsRasterLayer(fileName, baseName)
            QgsProject.instance().addMapLayer(SOIL)

            # Zoom to the layer
            zoom = SOIL.extent()
            self.canvas.setExtent(zoom)
            self.canvas.refresh()

            self.progressBar.setValue(50)

            provider = SOIL.dataProvider()
            SOIL_values = set()

            # Iterate over raster rows and columns
            for row in range(provider.xSize()):
                for col in range(provider.ySize()):
                    position = QgsPointXY(
                        SOIL.extent().xMinimum() + SOIL.rasterUnitsPerPixelX() * col,
                        SOIL.extent().yMaximum() - SOIL.rasterUnitsPerPixelY() * row,
                    )
                    value, result = provider.sample(position, 1)
                    if result:
                        SOIL_values.add(int(value))

            SOIL_sorted_values = sorted(SOIL_values)

            csv_path = FolderPath + "\MapSWAT\SWAT_INPUT_MAPS\SOIL\Soil_lookup.csv"
            with open(csv_path, "w", newline="") as csvfile:
                filewriter = csv.writer(csvfile)
                filewriter.writerow(["SOIL_ID", "SNAM"])
                for value in SOIL_sorted_values:
                    filewriter.writerow([value])

            # Read JSON file
            with open(json_path, "r") as json_file:
                json_data = json.load(json_file)
                value_to_landuse = {item["Value"]: item["Soil"] for item in json_data}

            # Read CSV file and paste values from CSV based on first column
            rows = []
            with open(csv_path, "r") as csv_file:
                reader = csv.DictReader(csv_file)

                for row in reader:
                    landuse_id = int(row["SOIL_ID"])
                    if landuse_id in value_to_landuse:
                        row["SNAM"] = value_to_landuse[landuse_id]
                    rows.append(row)
            with open(csv_path, "w", newline="") as csv_file:
                fieldnames = rows[0].keys()
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

            # Copy DSOLMap usersoil and taxonomy in local folder
            soil_usersoil = os.path.join(
                self.plugin_dir, "resources/DSOLMap_usersoil.csv"
            )
            soil_taxonomy = os.path.join(
                self.plugin_dir, "resources/DSOLMap_taxonomy.csv"
            )
            SOILpath = FolderPath + "\MapSWAT\SWAT_INPUT_MAPS\SOIL"
            shutil.copy(soil_usersoil, SOILpath)
            shutil.copy(soil_taxonomy, SOILpath)

        if self.checkBox_DEM.isChecked():
            DEMpath = FolderPath + "\MapSWAT\SWAT_INPUT_MAPS\DEM"

            DEMfile = self.comboBox_DEM.currentText()

            if DEMfile == "SRTM Digital Elevation Data 90m":
                DEM = ee.Image("CGIAR/SRTM90_V4")
                resolution = 90
                resolution_ini = 90

            if DEMfile == "NASADEM Digital Elevation 30m":
                DEM = ee.Image("NASA/NASADEM_HGT/001").select("elevation")
                resolution = 30
                resolution_ini = 30

            if DEMfile == "Copernicus DEM GLO-30m":
                DEM = ee.ImageCollection("COPERNICUS/DEM/GLO30").select("DEM").mosaic()
                resolution = 30
                resolution_ini = 30

            # Check the type of GEE object, if Geometry == True
            if isinstance(self.polygon, ee.geometry.Geometry):
                i = 0
                while i < 100:
                    # For geometry
                    try:
                        url = DEM.getDownloadURL(
                            {
                                "name": "DEM",
                                "scale": resolution,
                                "crs": crs_target_id,
                                "region": self.polygon.getInfo(),
                                "fileFormat": "GeoTIFF",
                            }
                        )
                        if resolution > resolution_ini:
                            QMessageBox.information(
                                None,
                                "Map Resolution Adjustment",
                                f"GEE request exceeds the limit of 32 MB. Raster resolution adjusted to {resolution} meters.",
                            )
                        break
                    except ee.ee_exception.EEException:
                        resolution += 10
                        i += 1

            # Check the type of GEE object, if FeatureCollection == True
            elif isinstance(self.polygon, ee.FeatureCollection):
                i = 0
                while i < 100:
                    # For feature collection
                    try:
                        url = DEM.getDownloadURL(
                            {
                                "name": "DEM",
                                "scale": resolution,
                                "crs": crs_target_id,
                                "region": self.polygon.geometry().bounds().getInfo(),
                                "fileFormat": "GeoTIFF",
                            }
                        )
                        if resolution > resolution_ini:
                            QMessageBox.information(
                                None,
                                "Map Resolution Adjustment",
                                f"GEE request exceeds the limit of 32 MB. Raster resolution adjusted to {resolution} meters.",
                            )
                        break
                    except ee.ee_exception.EEException:
                        resolution += 10
                        i += 1

            # Open the URL and download the zip
            save_path = os.path.join(FolderPath, "MapSWAT/SWAT_INPUT_MAPS/DEM/DEM.zip")
            response = requests.get(url)
            response.raise_for_status()
            with open(save_path, "wb") as f:
                f.write(response.content)

            # Extract the files of the zip file in the local folder
            dest_directory = os.path.dirname(save_path)
            with zipfile.ZipFile(save_path, "r") as zip_ref:
                zip_ref.extractall(dest_directory)

            # Select the tif file of the local folder
            files = os.listdir(dest_directory)
            for file in files:
                if file.endswith(".tif"):
                    fileName = os.path.join(dest_directory, file)

            # Add DEM in QGIS canvas
            fileInfo = QFileInfo(fileName)
            baseName = fileInfo.baseName()
            DEM = QgsRasterLayer(fileName, baseName)
            QgsProject.instance().addMapLayer(DEM)

            # Zoom to the layer
            zoom = DEM.extent()
            self.canvas.setExtent(zoom)
            self.canvas.refresh()

            self.progressBar.setValue(70)

        if self.lineX.isModified() and self.lineY.isModified():
            # Reproyectar OUTLET a crs_target
            params3 = {
                "INPUT": FolderPath + "/MapSWAT/WGS84/OUTLET_WGS84.shp",
                "TARGET_CRS": crs_target,
                "OUTPUT": FolderPath
                + "\MapSWAT\SWAT_INPUT_MAPS\INFO_GIS\OUTLET\OUTLET.shp",
            }
            processing.run("native:reprojectlayer", params3)

            # Añadir OUTLET reproyectado a QGIS
            layer = QgsVectorLayer(
                FolderPath + "\MapSWAT\SWAT_INPUT_MAPS\INFO_GIS\OUTLET\OUTLET.shp",
                "OUTLET",
                "ogr",
            )
            QgsProject.instance().addMapLayer(layer)

            self.progressBar.setValue(80)

        # Collect and clip GWFLOW inputs
        if self.checkBox_GWFLOW.isChecked():
            self.progressBar.setValue(85)
            GWFLOWpath = FolderPath + "/MapSWAT/SWAT_INPUT_MAPS/GWFLOW"

            # https://developers.google.com/earth-engine/apidocs/ee-featurecollection-getdownloadurl
            # Aquifer permeability from GLHYMPS
            GLHYMPS = ee.Image("projects/ee-alopez6/assets/GLHYMPS_logK_Ferr")
            resolution = 250
            resolution_ini = 250
            # Check the type of GEE object, if Geometry == True
            if isinstance(self.polygon, ee.geometry.Geometry):
                i = 0
                while i < 100:
                    # For geometry
                    try:
                        url = GLHYMPS.getDownloadURL(
                            {
                                "name": "GLHYMPS",
                                "scale": resolution,
                                "crs": crs_target_id,
                                "region": self.polygon.getInfo(),
                                "fileFormat": "GeoTIFF",
                            }
                        )
                        if resolution > resolution_ini:
                            QMessageBox.information(
                                None,
                                "Map Resolution Adjustment",
                                f"GEE request exceeds the limit of 32 MB. Raster resolution adjusted to {resolution} meters.",
                            )
                        break
                    except ee.ee_exception.EEException:
                        resolution += 10
                        i += 1
            # Check the type of GEE object, if FeatureCollection == True
            elif isinstance(self.polygon, ee.FeatureCollection):
                i = 0
                while i < 100:
                    # For feature collection
                    try:
                        url = GLHYMPS.getDownloadURL(
                            {
                                "name": "GLHYMPS",
                                "scale": resolution,
                                "crs": crs_target_id,
                                "region": self.polygon.geometry().bounds().getInfo(),
                                "fileFormat": "GeoTIFF",
                            }
                        )
                        if resolution > resolution_ini:
                            QMessageBox.information(
                                None,
                                "Map Resolution Adjustment",
                                f"GEE request exceeds the limit of 32 MB. Raster resolution adjusted to {resolution} meters.",
                            )
                        break
                    except ee.ee_exception.EEException:
                        resolution += 10
                        i += 1
            # Open the URL and download the zip
            save_path = os.path.join(
                FolderPath,
                "MapSWAT/SWAT_INPUT_MAPS/GWFLOW/GLHYMPS.zip",
            )
            response = requests.get(url)
            response.raise_for_status()
            with open(save_path, "wb") as f:
                f.write(response.content)
            # Extract the files of the zip file in the local folder
            dest_directory = os.path.dirname(save_path)
            with zipfile.ZipFile(save_path, "r") as zip_ref:
                zip_ref.extractall(dest_directory)

            # Convert raster to vector
            raster_GLHYMPS = os.path.join(
                FolderPath,
                "MapSWAT/SWAT_INPUT_MAPS/GWFLOW/GLHYMPS.b1.tif",
            )
            params = {
                "INPUT": raster_GLHYMPS,
                "BAND": 1,
                "FIELD": "logK_Ferr_",
                "EIGHT_CONNECTEDNESS": False,
                "EXTRA": "",
                "OUTPUT": "TEMPORARY_OUTPUT",
            }
            processing.runAndLoadResults("gdal:polygonize", params)

            # Path of temporary output
            shp = QgsProject.instance().mapLayersByName("Vectorized")[0]
            shpPath = shp.source()

            # Dissolve the shapefile
            shp_GLHYMPS = os.path.join(
                FolderPath,
                "MapSWAT/SWAT_INPUT_MAPS/GWFLOW/Aquifer_Permeability_GLHYMPS.shp",
            )
            params2 = {
                "INPUT": shpPath,
                "FIELD": ["logK_Ferr_"],
                "SEPARATE_DISJOINT": False,
                "OUTPUT": shp_GLHYMPS,
            }
            processing.run("native:dissolve", params2)

            # Change the 0 values of GLHYMPS
            GLHYMPS_layer = QgsVectorLayer(
                shp_GLHYMPS, "Aquifer_Permeability_GLHYMPS", "ogr"
            )
            QgsProject.instance().addMapLayer(GLHYMPS_layer)
            GLHYMPS_layer.startEditing()
            attr_index = GLHYMPS_layer.fields().indexFromName("logK_Ferr_")
            # Iterate through each feature in the layer
            for feature in GLHYMPS_layer.getFeatures():
                if feature["logK_Ferr_"] == 0:  # Check if the attribute's value is 0
                    # Update the feature's attribute value
                    GLHYMPS_layer.changeAttributeValue(feature.id(), attr_index, -1400)
            # Commit changes
            GLHYMPS_layer.commitChanges()

            # Remove temporary layers
            QgsProject.instance().removeMapLayer(shp.id())

            self.progressBar.setValue(90)

            # Aquifer Thickness from BDTICM_M_250m_ll
            BDTICM = ee.Image("projects/ee-alopez6/assets/BDTICM_M_250m_ll")
            resolution = 250
            resolution_ini = 250
            # Check the type of GEE object, if Geometry == True
            if isinstance(self.polygon, ee.geometry.Geometry):
                i = 0
                while i < 100:
                    # For geometry
                    try:
                        url = BDTICM.getDownloadURL(
                            {
                                "name": "BDTICM",
                                "scale": resolution,
                                "crs": crs_target_id,
                                "region": self.polygon.getInfo(),
                                "fileFormat": "GeoTIFF",
                            }
                        )
                        if resolution > resolution_ini:
                            QMessageBox.information(
                                None,
                                "Map Resolution Adjustment",
                                f"GEE request exceeds the limit of 32 MB. Raster resolution adjusted to {resolution} meters.",
                            )
                        break
                    except ee.ee_exception.EEException:
                        resolution += 10
                        i += 1
            # Check the type of GEE object, if FeatureCollection == True
            elif isinstance(self.polygon, ee.FeatureCollection):
                i = 0
                while i < 100:
                    # For feature collection
                    try:
                        url = BDTICM.getDownloadURL(
                            {
                                "name": "BDTICM",
                                "scale": resolution,
                                "crs": crs_target_id,
                                "region": self.polygon.geometry().bounds().getInfo(),
                                "fileFormat": "GeoTIFF",
                            }
                        )
                        if resolution > resolution_ini:
                            QMessageBox.information(
                                None,
                                "Map Resolution Adjustment",
                                f"GEE request exceeds the limit of 32 MB. Raster resolution adjusted to {resolution} meters.",
                            )
                        break
                    except ee.ee_exception.EEException:
                        resolution += 10
                        i += 1
            # Open the URL and download the zip
            save_path = os.path.join(
                FolderPath,
                "MapSWAT/SWAT_INPUT_MAPS/GWFLOW/BDTICM.zip",
            )
            response = requests.get(url)
            response.raise_for_status()
            with open(save_path, "wb") as f:
                f.write(response.content)
            # Extract the files of the zip file in the local folder
            dest_directory = os.path.dirname(save_path)
            with zipfile.ZipFile(save_path, "r") as zip_ref:
                zip_ref.extractall(dest_directory)

            raster_path = os.path.join(
                FolderPath,
                "MapSWAT/SWAT_INPUT_MAPS/GWFLOW/BDTICM.b1.tif",
            )

            # Add BDTICM in QGIS canvas
            fileInfo = QFileInfo(raster_path)
            baseName = fileInfo.baseName()
            BDTICM = QgsRasterLayer(raster_path, baseName)
            QgsProject.instance().addMapLayer(BDTICM)

            # Change nodata value (-32768) to 0
            raster_entry = QgsRasterCalculatorEntry()
            raster_entry.raster = BDTICM
            raster_entry.bandNumber = 1
            raster_entry.ref = "BDTICM@1"
            entries = [raster_entry]
            # Expression to replace -32768 with 0, keep other values as is
            expression = (
                f'("BDTICM@1" = -32768) * 0 + ("BDTICM@1" != -32768) * "BDTICM@1"'
            )
            # Output file path (adjust as needed)
            output_path = os.path.join(
                FolderPath,
                "MapSWAT/SWAT_INPUT_MAPS/GWFLOW/Aquifer_Thickness_BDTICM.tif",
            )
            # Perform the calculation
            calc = QgsRasterCalculator(
                expression,
                output_path,
                "GTiff",
                BDTICM.extent(),
                BDTICM.width(),
                BDTICM.height(),
                entries,
            )
            calc.processCalculation()
            # Load the output raster to QGIS canvas (optional)
            output_raster = QgsRasterLayer(output_path, "Aquifer_Thickness_BDTICM")
            QgsProject.instance().addMapLayer(output_raster)

            # Path of temporary output
            raster = QgsProject.instance().mapLayersByName("BDTICM")[0]
            # Remove temporary layers
            QgsProject.instance().removeMapLayer(raster.id())

        self.progressBar.setValue(95)
        self.progressBar.setValue(0)

        # Deactivate plugin
        self.showMinimized()

        # Message Process completed
        text = "Process completed successfully."
        msgINFO = QMessageBox()
        msgINFO.setWindowIcon(QIcon(":/imgMapSWAT/images/icon.png"))
        msgINFO.setWindowTitle("MapSWAT GEE")
        msgINFO.setText(text)
        msgINFO.setStandardButtons(QMessageBox.Ok)
        msgINFO.exec_()

        self.pushButton_BUFFER.setEnabled(False)
        self.pushButton_AUTOBASIN.setEnabled(False)
        self.pushButton_SWATinputs.setEnabled(False)

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
            # Clear CANVAS
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

    def infoDEM(self):
        DEMfile = self.comboBox_DEM.currentText()

        if DEMfile == "SRTM Digital Elevation Data 90m":
            url = "https://developers.google.com/earth-engine/datasets/catalog/CGIAR_SRTM90_V4"

        if DEMfile == "NASADEM Digital Elevation 30m":
            url = "https://developers.google.com/earth-engine/datasets/catalog/NASA_NASADEM_HGT_001"

        if DEMfile == "Copernicus DEM GLO-30m":
            url = "https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_DEM_GLO30"

        webbrowser.open(url)

    def infoLanduse(self):
        LULCfile = self.comboBox_LANDUSE.currentText()

        if LULCfile == "Copernicus Global Land Cover 2019":
            url = "https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_Landcover_100m_Proba-V-C3_Global"

        if LULCfile == "GlobCover: Global Land Cover Map 2009":
            url = "https://developers.google.com/earth-engine/datasets/catalog/ESA_GLOBCOVER_L4_200901_200912_V2_3"

        if LULCfile == "Copernicus CORINE Land Cover 1990 (only Europe)":
            url = "https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_CORINE_V20_100m"

        if LULCfile == "Copernicus CORINE Land Cover 2000 (only Europe)":
            url = "https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_CORINE_V20_100m"

        if LULCfile == "Copernicus CORINE Land Cover 2006 (only Europe)":
            url = "https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_CORINE_V20_100m"

        if LULCfile == "Copernicus CORINE Land Cover 2012 (only Europe)":
            url = "https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_CORINE_V20_100m"

        if LULCfile == "Copernicus CORINE Land Cover 2018 (only Europe)":
            url = "https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_CORINE_V20_100m"

        webbrowser.open(url)

    def infoSoil(self):
        SOILfile = self.comboBox_SOIL.currentText()

        if SOILfile == "DSOLMap: Digital Soil Open Land Map":
            url = "https://code.earthengine.google.com/?asset=projects/ee-alopez6/assets/DSOLMap"

        webbrowser.open(url)

    def infoAutobasin(self):
        url = "https://www.hydrosheds.org/products/hydrobasins"
        webbrowser.open(url)

    def infoGWFLOW(self):
        url1 = "https://code.earthengine.google.com/?asset=projects/ee-alopez6/assets/BDTICM_M_250m_ll"
        url2 = "https://code.earthengine.google.com/?asset=projects/ee-alopez6/assets/GLHYMPS_logK_Ferr"
        webbrowser.open(url1)
        webbrowser.open(url2)
