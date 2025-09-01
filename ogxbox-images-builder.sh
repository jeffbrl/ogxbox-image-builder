#!/bin/bash

usage() { echo "Usage: $0 [-t <output_image_type> raw|qcow2] [-s <size_in_GB>] [-c <c_zip_file>] [-e <e_zip_file] -o <output_image>" 1>&2; exit 1; }

while getopts ":s::o:c::e::t:" o; do
    case "${o}" in
        s)
            size=${OPTARG}
            ;;
        o)
            output=${OPTARG}
            ;;
        c)
            czip=${OPTARG}
            ;;
        e)
            ezip=${OPTARG}
            ;;
        t)
            image_type=${OPTARG}
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

if [[ -z "$output" ]]; then
    echo "Error: Specifying output image file with -o <file> is mandatory" >&2
    usage
    exit 1
fi

builder_args="/data/$output "

if [[ -z "$size" ]]; then
    echo "Output image size not specified...defaulting to 8G"
    size=8
    builder_args+="-s $size "
fi

if [[ -n "$czip" ]]; then
    builder_args+="-c /data/$czip "
fi

if [[ -n "$ezip" ]]; then
    builder_args+="-e /data/$ezip "
fi

if [[ -n "$image_type" ]]; then
    builder_args+="-t $image_type "
fi

docker run --rm -v $(pwd):/data jeffbrl/ogxbox-image-builder python3 /app/main.py $builder_args
