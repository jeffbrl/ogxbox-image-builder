FROM ubuntu:24.04 as builder
RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -qy \
        build-essential pkg-config libfuse-dev cmake git \
        python3 python3-pip pipx \
 && git clone https://github.com/mborgerson/fatx.git /usr/src/fatx

 WORKDIR /usr/src/fatx

# Build libfatx
RUN cmake -Blibfatx_build -Slibfatx \
 && cmake --build libfatx_build --target install

# Build fatxfs
RUN cmake -Bfatxfs -Sfatxfs -DCMAKE_INSTALL_PREFIX=/fatx \
 && cmake --build fatxfs --target install

COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt

RUN python3 -m pip install -r /app/requirements.txt --break-system-packages

RUN DEBIAN_FRONTEND=noninteractive apt remove -qy build-essential pkg-config cmake git \
&& apt clean -y && apt autoclean -y && apt autoremove -y \
&& rm -rf /var/lib/apt/lists/* && rm -rf /tmp/* && rm -rf /var/tmp/*