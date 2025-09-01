# OGXbox Image Builder (`ogxbox-image-builder`)

A python script to automate the creation of raw (`.img`) and QCOW2 (`.qcow2`) disk images for the original Xbox, suitable for use with emulators like xemu. The repository includes wrapper scripts in bash and powershell to simplify the execution of ogxbox-image-builder in a docker container

## Features

*   **Dual Format Output:** Generates both a raw `dd`-style image or a space-efficient QCOW2 image 
*   **Customizable Size:** Supports creating images of various standard Xbox partition sizes (~8GB, ~10GB, etc.).
*   **Flexible Filesystem Population:** Populates C and E drives with files from a zip archive (Optional)

## Execution Options

This program can be launched in three ways.

1. Docker container 
2. python interpreter

The docker container may be the easier method for less technically-inclined people as I've included
helper scripts in bash and powershell.

Using the python script directly is intended for advanced users. This option requires the compilation of the libfatx C library and fatxfs FUSE driver. 

## Prerequisites

This depends on which execution option you select.

If container, obviously you will need docker running in linux, WSL2, etc.

If you want to run from python:

*   **`qemu-img`**: For converting the raw image to the QCOW2 format.
*   **`libfatx`**: Development library for working with FATX filesystem.
*   **`fatxfs`**: Userspace FUSE driver for FATX filesystems. 

Note that I did not test the python script on Windows so YMMV.

## Usage

### Basic Syntax

```bash
./ogxbox-image-builder.sh -s <size_in_GB> -o <output_image> [-c c.zip] [-e e.zip] [ -t qcow2|raw]
```

Image size defaults to 8G.
Image type defaults to raw.
Conversion to qcow2 is very slow, use only if needed.

### Common Examples

1. Create an 8GB image and populate C and E drives with c.zip and e.zip respectively:

```bash
./ogxbox-image-builder.sh -o image.bin -c c.zip -e e.zip
```

2. Create an 16GB qcow2 image:

```bash
./ogxbox-image-builder.sh -s 16 -t qcow2 -o image.bin 
```

## Credits

This script performs very little work besides simple image creation and copying files into the image. All the heavy lifing is performing by mbogerson's https://github.com/mborgerson/fatx. All credit goes to him.

## License
This script is provided under the MIT License. Please ensure you legally own files you inject into the image.

## Disclaimer
This tool is intended for educational purposes and for use with software you have the legal right to modify and distribute. The authors are not responsible for any misuse of this script.