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

*	After installing the GEE plugin for the first time, you will see the following message. Users must register for a GEE account.
<p align="center">
<img src="resources/images/msg.png" alt="message" width="300">
</p>

* The **MapSWAT plugin** can now be installed. Launch the [executable](https://github.com/AdrLBallesteros/MapSWAT/releases) and activate the MapSWAT plugin from QGIS repository.
<p align="center">
<img src="resources/gifs/Install_MapSWAT.gif" alt="screenshot" width="500" style="display:inline-block">
<img src="resources/gifs/Activate_MapSWAT.gif" alt="screenshot" width="500" style="display:inline-block">
</p>
  
## Key Points

* MapSWAT is a single-use program, which means that when the program is closed all generated files will be deleted from QGIS canvas. However, all files will be still available in the MapSWAT folder.
  
* MapSWAT will only create the selected input maps, so remember to tick the box for each input map to generate them.
  
* If a python error appears during the use of MapSWAT, it is recommended to reboot the QGIS program to fix it. If it continues to be displayed, please  <a href="#contact">contact me</a>.

## How To Use

1.	Click on the MapSWAT button of the QGIS toolbar to open the MapSWAT plugin. You will be prompted to select the version of MapSWAT you want to use.

<p align="center">
<img src="resources/images/1.png" alt="1" width="300">
</p>

> **MapSWAT v3.0**: This is the standard version of MapSWAT. Users can import their own raster maps and prepare them in QSWAT or QSWAT+ format.

> **MapSWAT GEE**: This is the connected to [Google Earth Engine (GEE)](https://earthengine.google.com/) version of MapSWAT. Users must first sign up for a GEE account and install the GEE plugin from QGIS repository.

2.  Before going to the selected MapSWAT window, users also have to indicate a path to save the MapSWAT folder.

<p align="center">
<img src="resources/images/3.png" alt="3" width="300">
</p>

3.  Both versions are structured in the same way.

<p align="center">
<img src="resources/images/4-standard.png" alt="4-standard" width="300" style="display:inline-block">
<img src="resources/images/5-GEE.png" alt="5-GEE" width="300" style="display:inline-block">
</p>
   
4.  In the first step users can insert or select raster layers such as, a digital elevation map (DEM), a land use map (LANDUSE) and a soil map (SOIL). To do so, users must first tick the box for each SWAT input map they want to obtain.

## Credits

This software uses the following open source packages:

* [**QGIS**](https://github.com/qgis/QGIS)
* [**qgis-earthengine-plugin**](https://github.com/gee-community/qgis-earthengine-plugin)

## Contact

If you have feedback or suggestions, please contact me at **alopez6@ucam.edu**.

## Support

If you find this plugin useful, or if it has saved you time in your work, consider supporting it by inviting me for a coffee. Thanks! 😊

<p align="center">
<a href="https://www.buymeacoffee.com/alopez6" target="_blank"><img src="images/coffee.png" alt="Buy Me A Coffee" width="200"></a>
</p>

