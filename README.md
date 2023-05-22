# Protobuf-generator examples written in python

This repository contains the code for a protoc code-generator tutorial:
https://medium.com/@davidgroemling/create-and-run-a-protobuf-plugin-9471e16e8ad

## Install protoc

To run the examples, you need to install protoc. I recommend using a package manager like brew or apt to install it, but
you can also download the binary from the official repo, following the instructions
here: https://github.com/protocolbuffers/protobuf#protocol-compiler-installation

# Run the hello-world example

The hello-world example can be found in hello_world_generator. To setup all the dependencies in a virtual environment,
execute these commands:

```commandline
cd hello_world_generator
python3 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
```

Next, create a direcotry for the generator output:

```commandline
mkdir generated
```

Then run protoc with the plugin:

```commandline
protoc -I../proto \
       ../proto/hello_world.proto \
       --python_out=generated \
       --hello-world_out=generated \
       --plugin=protoc-gen-hello-world=hello_world_generator.py
```
