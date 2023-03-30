# pykrakenfiles
Package to upload file(s) with KrakenFiles public API

## Installation

Windows:

```
pip install pykrakenfiles
```

Linux/Mac OS:

```
pip3 install pykrakenfiles
```

## Example

```python
from pykrakenfiles import Krakenfiles

kraken = Krakenfiles(api_key='API_KEY')
file_path = 'path/image.png'
kraken.upload(file_path)
print(kraken.uploads)
```
```
Uploaded: image.png
Link: https://krakenfiles.com/view/iwfiifwi/file.html
[{'url': 'https://krakenfiles.com/view/iwfiifwi/file.html', 'hash': '0oxD8LP7LQ', 'title': 'image.png', 'size': '5.48 MB', 'folderId': None}]
```

# Documentation

[KrakenFiles API](https://krakenfiles.com/developers/api/upload)

`kraken = Krakenfiles(api_key=None|API_KEY)` | Create instance of Krakenfiles, the api_key is not required.

`kraken.upload('image.png')` | Upload a file or list of files to Krakenfiles. Take file path as parameter.
File path can be a string or a list of file paths

You can configure `progress_bar=True|False` and `show_filename=True|False` when uploading

It return a list of uploads `kraken.uploads`