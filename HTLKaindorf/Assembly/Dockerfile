FROM ubuntu:22.04

RUN apt -y update && apt -y upgrade

RUN apt-get install -y vim python3 python3-pip ninja-build clang nasm

# rizin installation
RUN pip3 install meson
RUN git clone https://github.com/rizinorg/rizin root/rizin
RUN cd root/rizin && meson setup build
RUN cd root/rizin && meson compile -C build
RUN cd root/rizin && meson install -C build

# Commands:
# docker build -t assembly .
# docker run -it assembly /bin/bash

