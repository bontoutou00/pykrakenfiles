import sys
from pathlib import Path
from requests import session, exceptions
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
        self.file_name = None
        self.total_size = None
        self.headers = {'Accept': 'application/json'}
        self.uploads = []
        self.session = session()

    def get_server(self):
        """ The get_server function is used to get the server url and access token."""
        r = self.session.get('https://krakenfiles.com/api/server/available', headers=self.headers, timeout=20)
        r_dict = r.json()
        if r.status_code == 200:
            self.server_url = r_dict['data']['url']
            self.server_access_token = r_dict['data']['serverAccessToken']
        else:
            print(f'Error: {r_dict}')

    def upload(self, file_path, progress_bar: bool = True, show_filename : bool = True):
        """The upload function takes a file path as an argument and uploads the file(s) to the server.\n
        Args:
            file_path: str / list Specify the file path of the file you want to upload
            progress_bar: bool Specify if the progress bar is whon or not"""
        if isinstance(file_path, str):
            file_path = [file_path]
        for file in file_path:
            file = Path(file)
            self.file_name = file.name
            self.total_size = file.stat().st_size
            self.get_server()
            if progress_bar is False:
                show_progress = 0
            else:
                show_progress = None
            if show_filename:
                desc = self.file_name
            else:
                desc = None
            with tqdm(desc=desc, total=self.total_size, unit="B", unit_scale=True, unit_divisor=1024, file=sys.stdout, leave=True, ncols=show_progress) as progress: ## https://stackoverflow.com/a/67726532/21447299
                e = MultipartEncoder(
                fields={'serverAccessToken': self.server_access_token,
                        'file': (self.file_name, open(file, 'rb'), 'text/plain')})
                m = MultipartEncoderMonitor(e, lambda monitor: progress.update(monitor.bytes_read - progress.n))
                if self.api_key:
                    headers = {'Content-Type': m.content_type, 'X-AUTH-TOKEN': self.api_key}
                else:
                    headers = {'Content-Type': m.content_type}
                try:
                    r = self.session.post(self.server_url, data=m, headers=headers, timeout=20)
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
                        self.uploads.append(r_dict['data'])
                    else:
                        print(f'Error: {r_dict}')
