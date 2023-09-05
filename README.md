<h1 align="center">
  <br>
  <a><img src="resources/images/MapSWAT.svg" alt="MapSWAT" width="250"></a>
  <br>
  MapSWAT
  <br>
</h1>

<h4 align="center">MapSWAT is a QGIS plugin for preparing QSWAT or QSWAT+ input maps</a>.</h4>

<p align="center">
  <a href="#installation">Installation</a> •
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#credits">Credits</a> •
  <a href="#contact">Contact</a> •
  <a href="#support">Support</a>
</p>

## Installation

### Download

* You can download [**here**](https://github.com/AdrLBallesteros/MapSWAT/releases) the latest installable version of MapSWAT for Windows.

### Initial Setup

*	Before installing the MapSWAT plugin, it is necessary to download and install [**QGIS 3.x**](https://www.qgis.org/en/site/index.html). It is recommended to use the long-term release version.

*	Launch a **QGIS 3 project**, navigate to **Plugins > Manage and Install Plugins > All**, and then search for [**"Google Earth Engine" plugin**](https://github.com/gee-community/qgis-earthengine-plugin).
<p align="center">
<img src="resources/gifs/Install-GEE.gif" alt="screenshot" width="700">
</p>

* The **MapSWAT plugin** can now be installed. Launch the [executable](https://github.com/AdrLBallesteros/MapSWAT/releases) and activate the MapSWAT plugin from QGIS repository.
<p align="center">
<img src="resources/gifs/Install_MapSWAT.gif" alt="screenshot" width="500" style="display:inline-block">
<img src="resources/gifs/Activate_MapSWAT.gif" alt="screenshot" width="500" style="display:inline-block">
</p>

*	After activating the **MapSWAT plugin** for the first time, you will see the following message. Users must register for a GEE account.
<p align="center">
<img src="resources/images/msg.png" alt="message" width="400">
</p>

## Key Points

* MapSWAT is a single-use program, which means that when the program is closed all generated files will be deleted from QGIS canvas. However, all files will be still available in the MapSWAT folder.
  
* MapSWAT will only create the selected input maps, so remember to tick the box for each input map to generate them.
  
* If a python error appears during the use of MapSWAT, it is recommended to reboot the QGIS program to fix it. If it continues to be displayed, please  <a href="#contact">contact me</a>.

## How To Use

1.	Click on the MapSWAT button of the QGIS toolbar to open the MapSWAT plugin. You will be prompted to select the version of MapSWAT you want to use.

<p align="center">
<img src="resources/images/1.PNG" alt="1" width="300">
</p>

> **MapSWAT v3.0**: This is the standard version of MapSWAT. Users can import their own raster maps and prepare them in QSWAT or QSWAT+ format.

> **MapSWAT GEE**: This is the connected to [Google Earth Engine (GEE)](https://earthengine.google.com/) version of MapSWAT. Users must first sign up for a GEE account and install the GEE plugin from QGIS repository.

2.  Before going to the selected MapSWAT version, users also have to indicate a path to save the MapSWAT folder.

<p align="center">
<img src="resources/images/3.PNG" alt="3" width="300">
</p>

3.  Both versions are structured in the same way.

<p align="center">
<img src="resources/images/4-standard.PNG" alt="4-standard" width="500" style="display:inline-block">
<img src="resources/images/5-GEE.PNG" alt="5-GEE" width="507" style="display:inline-block">
</p>
   
4.  In the first part of the MapSWAT window, users can insert or select the raster layers such as, a **digital elevation map (DEM)**, a **land use map (LANDUSE)** and a **soil map (SOIL)**. Remember to tick the box of the SWAT input map you want to obtain.
   
> Before moving on to the next part, users can also introduce an outlet point coordinates to easily locate the study area in the map canvas. This will unlock additional options such as **BUFFER CLIP** or **AUTOBASIN CLIP**.

<p align="center">
<img src="resources/gifs/Standard_Example_Part1.gif" alt="Standard_Example_Part1.gif" width="500" style="display:inline-block">
<img src="resources/gifs/GEE_Example_Part1.gif" alt="GEE_Example_Part1.gif" width="507" style="display:inline-block">
</p>

5.  When previous steps have been done, users have to click on **ADD LAYERS** or **GET MAPS** to activate the following part of the MapSWAT plugin.

> Additionally, a **MERGE DEMs** option has been included in the standard version of MapSWAT. To use it, user must click on the MERGE DEMs button, select the DEM layers (.tif) to merge and click on the OPEN button.

<p align="center">
<img src="resources/gifs/Merge_DEMs.gif" alt="Merge_DEMs" width="500">
</p>

6.  **CLIPPING OPTIONS**: MapSWAT includes several options for clipping raster layers.
  * **MANUAL CLIP**: Allows users to manually draw an extraction mask (POLYGON).
  
<p align="center">
<img src="resources/gifs/Manual_clip.gif" alt="Manual_clip.gif" width="500">
</p>

> After drawing the extraction mask, right-click the mouse and a window for indicating the FID number will appear. Set any number, for example 1, and click the **OK button**.

  * **SHAPEFILE CLIP**: Allows users to select any shapefile as an extraction mask (POLYGON).
  
<p align="center">
<img src="resources/gifs/Shapefile_clip.gif" alt="Shapefile_clip.gif" width="500">
</p>

  * **BUFFER CLIP**:  With this option, an extraction mask (POLYGON) is automatically created around the outlet point. To do so, users have to indicate the buffer distance in kilometers (10 Km by default).
  
<p align="center">
<img src="resources/gifs/Buffer_clip.gif" alt="Buffer_clip.gif" width="500">
</p>

 * **AUTOBASIN CLIP**:  This option is **only available in the GEE version**, a predefined basin is obtained from [HydroSHEDS Basins](https://www.hydrosheds.org/products/hydrobasins) to be used as an extraction mask (POLYGON).
  
<p align="center">
<img src="resources/gifs/Autobasin_clip.gif" alt="Autobasin_clip.gif" width="500">
</p>

7. **SWAT INPUT MAPS CRS**:  This is the last part of the MapSWAT window, in this step users have to indicate a target CRS to reproject all generated maps.

<p align="center">
<img src="resources/gifs/SWAT_Input_Maps.gif" alt="SWAT_Input_Maps.gif" width="500">
</p>
   
> **The target CRS needs to be a metric CRS**, for example UTM.

8.  Now, the created raster layers **(“DEM”, “LANDUSE” and “SOIL”)** can be found in the QGIS canvas.

<p align="center">
<img src="resources/images/6.PNG" alt="6.PNG" width="700">
</p>

> Additionally, for the LANDUSE and SOIL input maps a template of their **LOOKUP tables** is automatically created. 

<p align="center">
<img src="resources/images/7.PNG" alt="7.PNG" width="300">
</p>

9.  When closing, a warning window is displayed to remind users that the QGIS canvas will be cleared and all uploaded files will disappear.

<p align="center">
<img src="resources/gifs/Closing.gif" alt="Closing.gif" width="650">
</p>   

## Credits

This software uses the following open source packages:

* [**QGIS**](https://github.com/qgis/QGIS)
* [**qgis-earthengine-plugin**](https://github.com/gee-community/qgis-earthengine-plugin)

## Contact

If you have feedback or suggestions, please contact me at **alopez6@ucam.edu**.

## Support

If you find this plugin useful, or if it has saved you time in your work, consider supporting it by inviting me for a coffee. Thanks! 😊

<p align="center">
<a href="https://www.buymeacoffee.com/alopez6" target="_blank"><img src="resources/images/yellow-button.png" alt="Buy Me A Coffee" width="120"></a>
</p>

