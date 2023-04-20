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
# Documentation module

[KrakenFiles API](https://krakenfiles.com/developers/api/upload)

`kraken = Krakenfiles(api_key=None|API_KEY)` | Create instance of Krakenfiles, the api_key is not required.

When creating an instance of `Krakenfiles()` with an API_KEY it also populate `kraken.files` with a list of the files from the account.

`kraken.upload('image.png')` | Upload a file or list of files to Krakenfiles. Take file path as parameter.
File path can be a string or a list of file paths

You can configure `progress_bar=True|False` and `show_filename=True|False` when uploading

It return a list of uploads `kraken.uploads`

### Example

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

# Documentation CLI
## pykrakenfiles
```console
usage: pykrakenfiles [-h] [-a API_KEY] -p PATHS [PATHS ...] [--output_filetype {yaml,txt}] [-o OUTPUT_DEST] [-r {0,1,2,3,4,5}] [--show_progress_bar] [--hide_progress_bar] [--show_filename] [--hide_filename]

Upload files to KrakenFiles.

options:
  -h, --help            show this help message and exit
  -a API_KEY, --api_key API_KEY
                        API Key from KrakenFiles account. File limit is 2GB instead of 1GB when using an account. Default = None
  -p PATHS [PATHS ...], --paths PATHS [PATHS ...]
                        Paths to look in for files to upload. Can be multiple paths
  --output_filetype {yaml,txt}
                        Output file type. Default = yaml
  -o OUTPUT_DEST, --output_dest OUTPUT_DEST
                        Output path destination. Default = Current working directory
  -r {0,1,2,3,4,5}, --retries {0,1,2,3,4,5}
                        How many times to re-attempt failed uploads. Default = 0.
  --show_progress_bar   Show the progress bar. (Default)
  --hide_progress_bar   Hide the progress bar.
  --show_filename       Show the filename. (Default)
  --hide_filename       Hide the filename.

```
### Example 
Upload `test.txt` with `API_KEY` and output the link to a yaml file in `C:\Users\Downloads`, retry `3` times if the upload fail.
```console
pykrakenfiles -a <API_KEY> -p c:\Users\test.txt -r 3 --hide_filename -o C:\Users\Downloads
```
## pykrakenfiles-list
```console
usage: pykrakenfiles-list [-h] -a API_KEY [--files] [--folders] [-o OUTPUT]

List files/folders from a KrakenFiles account.

options:
  -h, --help            show this help message and exit
  -a API_KEY, --api_key API_KEY
                        API Key from KrakenFiles account.
  --files               List files from KrakenFiles account.
  --folders             List folders from KrakenFiles account.
  -o OUTPUT, --output OUTPUT
                        Output path destination. Default = Current working directory
```
Will return a list of files/folders from the account specified and export them to a yaml file.
### Example 
List all the `files` from `API_KEY` and output them to a yaml file in `C:\Users\Downloads`.
```console
pykrakenfiles-list -a <API_KEY> --files -o C:\Users\Downloads
```
