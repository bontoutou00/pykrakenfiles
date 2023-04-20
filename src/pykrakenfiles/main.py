import sys
from pathlib import Path

from requests import exceptions, session, adapters
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from tqdm import tqdm


def convert_bytes(size):
    """ The convert_bytes function converts bytes to KB, MB or GB. """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f'{size:3.2f} {x:s}'
        size /= 1024.0

class Krakenfiles:
    def __init__(self, api_key: str = None) -> None:
        self.api_key = api_key
        self.server_url = None
        self.server_access_token = None
        self.total_size = None
        self.headers = {'Accept': 'application/json'}
        self.uploads = {}
        self.session = session()
        if self.api_key:
            self.list_files(self.api_key)

    def get_server(self):
        """ The get_server function is used to get the server url and access token."""
        r = self.session.get(
            'https://krakenfiles.com/api/server/available',
            headers=self.headers, 
            timeout=20
            )
        r_dict = r.json()
        if r.status_code == 200:
            self.server_url = r_dict['data']['url']
            self.server_access_token = r_dict['data']['serverAccessToken']
        else:
            print(f'Error: {r_dict}')
    
    def list_files(self, api_key: str):
        """ The list_files function is used to return a list of all the files."""
        headers = {'X-AUTH-TOKEN': api_key}
        r = self.session.get(
            'https://krakenfiles.com/api/file',
            headers=headers, 
            timeout=20
            )
        r_dict = r.json()
        if r.status_code == 200:
            self.files = r_dict['data']
            return self.files
        else:
            if r_dict['message'] == 'Invalid credentials.':
                raise InvalidApiKey('Invalid credentials.')
            else:
                print(f'Error: {r_dict}')
    
    def list_folders(self, api_key: str):
        """ The list_folders function is used to return a list of all the folders."""
        headers = {'X-AUTH-TOKEN': api_key}
        r = self.session.get(
            'https://krakenfiles.com/api/folder',
            headers=headers, 
            timeout=20
            )
        r_dict = r.json()
        if r.status_code == 200:
            self.folders = r_dict['data']
            return self.folders
        else:
            if r_dict['message'] == 'Invalid credentials.':
                raise InvalidApiKey('Invalid credentials.')
            else:
                print(f'Error: {r_dict}')
    
    def check_size(self, file):
        """ The check_size function is used to check if the file is not too large."""
        self.total_size = file.stat().st_size
        if self.api_key:
            print('File limit is 2GB!')
            if self.total_size > 2097152000:
                raise FileTooLarge('File exceeds 2 GB.')
        else:
            print('File limit is 1GB!')
            if self.total_size > 1048576000:
                raise FileTooLarge('File exceeds 1 GB.')

    def upload(
        self,
        file_path, 
        progress_bar: bool = True,
        show_filename : bool = True,
        max_retries: int = 0
        ):
        """The upload function takes a file path
        as an argument and uploads the file(s) to the server.\n
        Args:
            file_path: str / list Specify the file path of the file you want to upload
            progress_bar: bool Specify if the progress bar is whon or not"""
        self.session.mount(
            'https://',
            adapters.HTTPAdapter(
            max_retries=max_retries
            )
        )
        if isinstance(file_path, str):
            file_path = [file_path]
        for file in file_path:
            file = Path(file)
            self.check_size(file)
            self.get_server()
            if progress_bar is False:
                show_progress = 0
            else:
                show_progress = None
            if show_filename:
                desc = file.name
            else:
                desc = None
            with tqdm(
                desc=desc,
                total=self.total_size,
                unit="B",
                unit_scale=True, 
                unit_divisor=1024,
                file=sys.stdout, 
                leave=True, 
                ncols=show_progress
                ) as progress: ## https://stackoverflow.com/a/67726532/21447299
                e = MultipartEncoder(
                    fields = {
                        'serverAccessToken': self.server_access_token,
                        'file': (
                            file.name, open(file, 'rb'), 'text/plain'
                            )
                        }
                    )
                m = MultipartEncoderMonitor(
                    e,
                    lambda monitor: progress.update(
                        monitor.bytes_read - progress.n
                        )
                    )
                if self.api_key:
                    headers = {
                        'Content-Type': m.content_type,
                        'X-AUTH-TOKEN': self.api_key
                        }
                else:
                    headers = {'Content-Type': m.content_type}
                try:
                    r = self.session.post(
                        self.server_url,
                        data=m,
                        headers=headers,
                        timeout=20
                        )
                except (exceptions.SSLError, exceptions.ConnectionError) as error:
                    progress.close()
                    print(error)
                else:
                    r.raise_for_status()
                    progress.close()
                    r_dict = r.json()
                    if r.status_code == 200:
                        print(f"\nUploaded: {r_dict['data']['title']}")
                        print(f"Link: {r_dict['data']['url']}")
                        r_dict['data']['size'] = convert_bytes(r_dict['data']['size'])
                        self.uploads.update(r_dict['data'])
                    else:
                        print(f'Error: {r_dict}')

class InvalidApiKey(Exception):
    '''Exception when the api_key is invalid'''
class FileTooLarge(Exception):
    '''Exception when the file is larger than accepted'''
