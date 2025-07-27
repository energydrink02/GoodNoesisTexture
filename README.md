**GoodNoesisTexture** is a noesis script to view and extract textures from all games developed by Heavy Iron Studios using the good engine. Notable games running on this engine are:
* Ratatouille (PS3, X360)
* Wall-E (PS3, X360, Wii)
* Up (PS3, X360, Wii)
* SpongeBob's Truth or Square (X360, Wii)
* Family Guy: Back to the Multiverse (PS3, X360)

## Installation
1. Download [Noesis](https://richwhitehouse.com/index.php?content=inc_projects.php&filemirror=noesisv4474.zip) and extract somewhere (no installation required)
2. Download this repo (Releases -> Source code)
3. Copy **fmt_GoodEngineTexture.py** into `/plugins/python/`

## Usage
* Click on any *.ho file and it will prompt you to select an output directory. Personally, I had issues using the dialog so prefer to set the path manually if you have issues too (and don't forget to put a "\\" at the end of the path)
* Noesis will extract all textures as "*.ptex_" files, which are labeled as "GoodEngine PS3/Xbox360/Wii Texture" in noesis. You can now click on any ptex file to view and extract them.

## Optional: Wii Textures
* If you want to view and extract Wii textures, [download **lib_zq_nintendo_tex.py** from this repo](https://github.com/Zheneq/Noesis-Plugins) and copy it to the same noesis plugins directory.
    * [Direct link](https://raw.githubusercontent.com/Zheneq/Noesis-Plugins/01ecf7243b95748a0a6950eb588b69152cf69d46/lib_zq_nintendo_tex.py) (Right-Click -> Save as...)

> [!NOTE]
> Non-UI textures are mirrored. This is not an issue with this script or noesis.