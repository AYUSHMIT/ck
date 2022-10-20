FROM registry.access.redhat.com/ubi9
SHELL ["/bin/bash", "-c"]
ARG CM_GH_TOKEN

# Notes: https://runnable.com/blog/9-common-dockerfile-mistakes
# Install system dependencies
RUN dnf update -y
RUN dnf install -y python3 python-pip git wget sudo binutils

# Install python packages
RUN python3 -m pip install cmind requests

# Setup docker environment
ENTRYPOINT ["/bin/bash", "-c"]
ENV TZ=US/Pacific
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ >/etc/timezone

# Setup docker user
RUN groupadd cm
RUN useradd  -g cm --create-home --shell /bin/bash cmuser
RUN echo "cmuser ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
USER cmuser:cm
WORKDIR /home/cmuser

# Download CM repo for scripts
RUN cm pull repo mlcommons@ck

# Install all system dependencies
RUN cm run script --quiet --tags=get,sys-utils-cm

# Run command
RUN cm run script --tags=app,mlperf,inference,reference,_resnet50,_onnxruntime,_cpu,_cpp --adr.compiler.tags=gcc