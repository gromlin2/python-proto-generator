import os
import sys
from pathlib import Path

sys.path.append(str(Path(os.path.abspath(__file__)).parent.parent))

from google.protobuf.descriptor_pb2 import (
    FileDescriptorProto,
)

from descriptor_counters import count_messages, count_enums, count_services


def test_messages():
    fd = FileDescriptorProto()
    fd.message_type.add()
    fd.message_type.add()
    fd.message_type.add()
    assert count_messages(fd) == 3


def test_messages_embedded():
    fd = FileDescriptorProto()
    fd.message_type.add()
    message_with_embedded = fd.message_type.add()
    message_with_embedded.nested_type.add()
    message_with_embedded.nested_type.add()
    assert count_messages(fd) == 4


def test_enums():
    fd = FileDescriptorProto()
    fd.enum_type.add()
    fd.enum_type.add()
    fd.enum_type.add()
    fd.enum_type.add()
    assert count_enums(fd) == 4


def test_embedded_enums():
    fd = FileDescriptorProto()
    message_with_embedded = fd.message_type.add()
    message_with_embedded.enum_type.add()
    message_with_embedded.enum_type.add()
    assert count_enums(fd) == 2


def test_service_no_service():
    fd = FileDescriptorProto()
    fd.service.add()
    fd.service.add()
    assert count_services(fd) == 2


def test_service_two_services():
    fd = FileDescriptorProto()
    fd.service.add()
    fd.service.add()
    assert count_services(fd) == 2
