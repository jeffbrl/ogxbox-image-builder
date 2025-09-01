import argparse
import os
import re
import subprocess
import sys
import tempfile
import zipfile

from pathlib import Path
from typing import Generator, Tuple

from pyfatx import Fatx

DEFAULT_DISK_SIZE = 8*1024*1024*1024

parser = argparse.ArgumentParser(description='Xemu image creator')
parser.add_argument('image_filename', help='Name of the image file to create')
parser.add_argument('-c', type=str, help='Zip archive for C drive')
parser.add_argument('-e', type=str, help='Zip archive for E drive')
parser.add_argument('-f', type=str, help='Zip archive for F drive')
parser.add_argument('-s', '--size', type=int, default = None, help='Desired image size in GB')
parser.add_argument('-t', '--type', type=str, choices=["qcow2", "raw"], default="raw", help="Type of output disk (qcow2, raw). Defaults to raw")

args = parser.parse_args()

def is_vfat_filename_valid(filename):
    """
    Check if a filename is valid for VFAT filesystem.
    
    Args:
        filename: The filename to validate (without path)
    
    Returns:
        Tuple of (is_valid, error_message)
    """
  
    if not filename:
        return False, "Filename cannot be empty"
    
    if len(filename) > 42: 
        return False, "Filename too long (max 42 characters)"
    
    invalid_chars = r'[<>:"/\\|?*]'
    if re.search(invalid_chars, filename):
        return False, "Contains invalid characters: < > : \" / \\ | ? *"
    
    # Check for control characters (ASCII 0-31)
    if re.search(r'[\x00-\x1f]', filename):
        return False, "Contains control characters"
    
    return True, "Valid VFAT filename"


def process_zip_archive(zip_file_path: str) -> Generator:
    """
    Unzips an archive and reads each file's content into a bytes object.

    Args:
        zip_file_path (str): Path to the .zip file.

    Returns:
        Tuple of filename (str), file_contents (bytes)
    """
    file_contents = {}

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        file_list = zip_ref.namelist()

        for file_name in file_list:
            yield (file_name, zip_ref.read(file_name))

def main() -> int:
    
    if os.path.exists(args.image_filename):
        os.remove(args.image_filename)

    if args.size is None:
        disk_size = DEFAULT_DISK_SIZE
        
    elif args.size < 8 or args.size > 2000:
        print("Min disk size: 8 GB. Max disk size: 2000")
        return 1
    
    else:
        disk_size = args.size * 1024 * 1024 * 1024 # convert to GB
     
    temp_disk_filename = args.image_filename + '.tmp'
    
    try:
        os.unlink(temp_disk_filename)
    except FileNotFoundError:
        pass

    print(f'Creating {int(disk_size / 1024 / 1024 / 1024)}G image...')   
    Fatx.create(temp_disk_filename, disk_size)
    fat_c = Fatx(temp_disk_filename, drive='c')
    fat_e = Fatx(temp_disk_filename, drive='e')
    #fat_f = Fatx(args.image_filename, drive='f')
    
    data = []
    
    if args.c:
        data.append((args.c, fat_c))
        
    if args.e:
        data.append((args.e, fat_e))
        
    #if args.f:
    #    data.append(args.f, fat_f)
    
        
    for zip_archive, fat in data:
        
        try:

            for entry_from_archive,file_content in process_zip_archive(zip_archive):
        
                name = Path(entry_from_archive).name
                valid, error = is_vfat_filename_valid(name)
                if not valid:
                    print(f"{error}: {entry_from_archive}")
                    continue
        
                # Check for directory
                try:
                    if entry_from_archive[-1] == '/':
                        fat.mkdir(entry_from_archive[:-1])
                    else:
                        fat.write(path=entry_from_archive, content=file_content)
                except AssertionError:
                    print(f"AssertionError on write(): {entry_from_archive}")
                    continue
            del(fat)

        except FileNotFoundError:
            print(f"{zip_archive} not found. Skipping...")
            continue

    # Convert to sparse qcow2 (slow)
    if args.type == 'qcow2':
        command = f"qemu-img convert -f raw -O qcow2 {temp_disk_filename} {args.image_filename}"
        retval = subprocess.run(command, shell=True, capture_output=True)
        if retval.returncode == 0:
            print("Conversion to qccow2 succeeded.")    
        else:
            print("Conversion to qccow2 failed.")
            print(retval.stderr)
        
        try:
            os.unlink(temp_disk_filename)
        except FileNotFoundError:
            pass
    else:
        os.rename(temp_disk_filename, args.image_filename) 
    return 0

if __name__ == '__main__':
    sys.exit(main())
