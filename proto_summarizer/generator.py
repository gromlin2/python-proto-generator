#!/usr/bin/env python3

import logging
import sys
from bs4 import BeautifulSoup as bs

from google.protobuf.compiler.plugin_pb2 import (
    CodeGeneratorResponse,
    CodeGeneratorRequest,
)

from google.protobuf.descriptor_pb2 import (
    FileDescriptorProto,
)

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


def count_string(count: int, reasons="unset") -> str:
    return "NO" if count == 0 else f"{count}"


def plural_s(count: int) -> str:
    return "" if count == 1 else "s"


def package_string(package_name: str) -> str:
    return (
        package_name
        if package_name
        else 'not defined, consider adding "package [name]" to your proto'
    )


def generate_for_proto(
    file_descriptor: FileDescriptorProto,
) -> CodeGeneratorResponse.File:
    file = CodeGeneratorResponse.File()
    file.name = file_descriptor.name.replace(".proto", ".html")

    dependency_count = len(file_descriptor.dependency)
    message_count = count_messages(file_descriptor)
    enum_count = count_enums(file_descriptor)
    service_count = count_services(file_descriptor)
    method_count = count_methods(file_descriptor)

    content = f"""
    <h1>Summary of {file_descriptor.name}</h1>
    Nice protobuf you defined there using {file_descriptor.syntax} syntax.<br />
    Its package is {package_string(file_descriptor.package)}. <br />
    It is importing {count_string(dependency_count)} other protobuf{plural_s(dependency_count)}. <br />
    <br />
    {file_descriptor.name} contains
    <ul>
      <li>{count_string(message_count)} message{plural_s(message_count)}</li>
      <li>{count_string(enum_count)} enum{plural_s(enum_count)}</li>
      <li>{count_string(service_count)} service{plural_s(service_count)}</li>
      <li>{count_string(method_count, "method")} method{plural_s(message_count)}</li>
    </ul>
    """

    file.content = bs(content, features="html.parser").prettify()

    return file


if __name__ == "__main__":
    request = CodeGeneratorRequest.FromString(sys.stdin.buffer.read())
    response = CodeGeneratorResponse()

    for proto_file in request.proto_file:
        if proto_file.name in request.file_to_generate:
            logger.info(f"Generating code for {proto_file.name}")
            f = generate_for_proto(proto_file)
            response.file.append(f)

    sys.stdout.buffer.write(response.SerializeToString())
