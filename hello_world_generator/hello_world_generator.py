#!/usr/bin/env python3

import sys

from google.protobuf.compiler.plugin_pb2 import CodeGeneratorResponse

if __name__ == "__main__":
    response = CodeGeneratorResponse()
    generated_file = response.file.add()
    generated_file.name = "hello_world.txt"
    generated_file.content = "Greetings, world!"
    sys.stdout.buffer.write(response.SerializeToString())
