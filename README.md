# CanteenMenuAllesLeckerEssen

With the script `getmenudata.py`, the canteen menus for the current and the following month are read out from PDF files from a [caterer in Halle, Germany](https://www.alles-lecker-essen.de) and converted into a JSON file.

This is a special use case and will hardly be of interest to anyone. If so, I am grateful for suggestions for improvement or a pull request.

## Installation

### Clone / Download

```sh
git clone https://github.com/KristjanESPERANTO/CanteenMenuAllesLeckerEssen/
```

#### Install requirements

```sh
# To download and parse the website
pip install requests beautifulsoup4
# To handle the pdf files
pip install "camelot-py[base]"
sudo apt-get install python3-opencv
# To handle tables and export json
pip install pandas
# The following row maybe isn't necessary
sudo apt-get install libatlas-base-dev
```

### Test

```sh
cd CanteenMenuAllesLeckerEssen
python3 getmenudata.py
```

## ToDo

- MagicMirror² as an example with screenshot
