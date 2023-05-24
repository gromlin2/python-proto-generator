#!/usr/bin/env python3

import logging
import sys

from google.protobuf.compiler.plugin_pb2 import (
    CodeGeneratorResponse,
    CodeGeneratorRequest,
)
from google.protobuf.descriptor_pb2 import (
    FileDescriptorProto,
)

import html_template
from descriptor_counters import (
    count_messages,
    count_enums,
    count_services,
    count_methods,
)

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def generate_for_proto(
    file_descriptor: FileDescriptorProto,
) -> CodeGeneratorResponse.File:
    """Generates code for one specific proto-file"""
    generated_file = CodeGeneratorResponse.File()
    generated_file.name = file_descriptor.name.replace(".proto", ".html")

    dependency_count = len(file_descriptor.dependency)
    message_count = count_messages(file_descriptor)
    enum_count = count_enums(file_descriptor)
    service_count = count_services(file_descriptor)
    method_count = count_methods(file_descriptor)

    generated_file.content = html_template.render(
        proto_path=file_descriptor.name,
        syntax=file_descriptor.syntax,
        package_name=file_descriptor.package,
        dependency_count=dependency_count,
        message_count=message_count,
        enum_count=enum_count,
        service_count=service_count,
        method_count=method_count,
    )

    return generated_file


if __name__ == "__main__":
    request = CodeGeneratorRequest.FromString(sys.stdin.buffer.read())
    response = CodeGeneratorResponse()

    for proto_file in request.proto_file:
        if proto_file.name in request.file_to_generate:
            logger.info(f"Generating code for {proto_file.name}")
            f = generate_for_proto(proto_file)
            response.file.append(f)

    sys.stdout.buffer.write(response.SerializeToString())
