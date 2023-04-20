import argparse
import os
from datetime import datetime
from pathlib import Path
from pprint import pprint

from yaml import dump

from .main import Krakenfiles


def main():
    parser = argparse.ArgumentParser(
        description='Upload files to KrakenFiles.'
        )
    parser.add_argument(
        '-a',
        '--api_key',
        default=None,
        help='API Key from KrakenFiles account. \
            File limit is 2GB instead of 1GB when using an account. \
            Default = None'
        )
    parser.add_argument(
        '-p', 
        '--paths',
        nargs='+',
        required=True,
        help='Paths to look in for files to upload. \
            Can be multiple paths'
        )
    parser.add_argument(
        '--output_filetype',
        choices=['yaml','txt'],
        default='yaml',
        help='Output file type. \
            Default = yaml'
        )
    parser.add_argument(
        '-o',
        '--output_dest',
        default=os.getcwd(),
        help='Output path destination. \
            Default = Current working directory'
        )
    parser.add_argument(
        '-r',
        '--retries',
        type=int,
        choices=[0, 1, 2, 3, 4, 5],
        default=0,
        help='How many times to re-attempt failed uploads. \
            Default = 0.'
        )
    parser.add_argument(
        '--show_progress_bar',
        dest='progress_bar',
        action='store_true',
        help='Show the progress bar. (Default)'
        )
    parser.add_argument(
        '--hide_progress_bar',
        dest='progress_bar',
        action='store_false',
        help='Hide the progress bar.'
        )
    parser.set_defaults(progress_bar=True)
    parser.add_argument(
        '--show_filename',
        dest='filename',
        action='store_true',
            help='Show the filename. (Default)'
        )
    parser.add_argument(
        '--hide_filename',
        dest='filename',
        action='store_false',
            help='Hide the filename.'
        )
    parser.set_defaults(filename=True)
    args = parser.parse_args()
    kraken = Krakenfiles(api_key=args.api_key)
    if args.paths:
        for path in args.paths:
            if os.path.isfile(path):
                kraken.upload(
                    path,
                    progress_bar=args.progress_bar,
                    show_filename=args.filename,
                    max_retries=args.retries
                    )
                if kraken.uploads:
                    output(
                        kraken,
                        file_type=args.output_filetype,
                        output_dest=args.output_dest
                        )
            else:
                files = os.listdir(path)
                print(f'Uploading {files}')                   
                for file in os.listdir(path):
                    file_path = os.path.join(path, file)
                    kraken.upload(
                        file_path,
                        progress_bar=args.progress_bar,
                        show_filename=args.filename,
                        max_retries=args.retries)
                    if kraken.uploads:
                        output(
                            kraken,
                            file_type=args.output_filetype,
                            output_dest=args.output_dest
                            )

def list():
    parser = argparse.ArgumentParser(
        description='List files/folders from a KrakenFiles account.'
        )
    parser.add_argument(
        '-a',
        '--api_key',
        required=True,
        help='API Key from KrakenFiles account.'
        )
    parser.add_argument(
        '--files',
        action='store_true',
        help='List files from KrakenFiles account.'
        )
    parser.add_argument(
        '--folders',
        action='store_true',
        help='List folders from KrakenFiles account.'
        )
    parser.add_argument(
        '-o',
        '--output',
        default=os.getcwd(),
        help='Output path destination. \
            Default = Current working directory'
        )
    args = parser.parse_args()
    kraken = Krakenfiles(api_key=args.api_key)
    date = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    if args.files:
        pprint(kraken.files)
        if kraken.files:
            path = Path(args.output, f'files_{date}.yaml')
            with open(
                path,
                'a+',
                encoding='utf8'
                ) as file:
                for entry in kraken.files:
                    dump([entry], file, sort_keys=False)
                print(f'Wrote files to {path}')
    if args.folders:
        kraken.list_folders(api_key=args.api_key)
        if kraken.folders:
            pprint(kraken.folders)
            path = Path(args.output, f'folders_{date}.yaml')
            with open(
                path,
                'a+',
                encoding='utf8'
                ) as file:
                for entry in kraken.folders:
                    dump([entry], file, sort_keys=False)
            print(f'Wrote folders to {path}')

def output(kraken, file_type, output_dest):
    kraken.uploads.update(
        {'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        )
    if file_type == 'yaml':
        path = Path(output_dest, 'krakenfiles_links.yaml')
        with open(
            path,
            'a+',
            encoding='utf8'
            ) as file:
            dump([kraken.uploads], file, sort_keys=False)
            print(f'Wrote link to {path}')
    elif file_type == 'txt':
        path = Path(output_dest, 'krakenfiles_links.txt')
        with open(
            path,
            "a+",
            encoding="utf8"
            ) as file:
            file.write(f"name: {kraken.uploads['title']}"
                        f"\nurl: {kraken.uploads['url']}"
                        f"\ndate: {kraken.uploads['date']}\n\n")
            print(f'Wrote link to {path}')
