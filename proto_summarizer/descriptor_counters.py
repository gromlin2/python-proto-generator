from typing import Union

from google.protobuf.descriptor_pb2 import (
    DescriptorProto,
    EnumDescriptorProto,
    FileDescriptorProto,
    ServiceDescriptorProto,
)


def count_messages(descriptor: Union[FileDescriptorProto, DescriptorProto]) -> int:
    if isinstance(descriptor, DescriptorProto):
        return len(descriptor.nested_type) + sum(
            [count_messages(nested) for nested in descriptor.nested_type]
        )

    if isinstance(descriptor, FileDescriptorProto):
        return len(descriptor.message_type) + sum(
            [count_messages(nested) for nested in descriptor.message_type]
        )
    raise TypeError("Only file and message descriptors are supported.")


def count_enums(
    descriptor: Union[FileDescriptorProto, DescriptorProto, EnumDescriptorProto]
) -> int:
    if isinstance(descriptor, DescriptorProto):
        return len(descriptor.enum_type) + sum(
            [count_enums(nested) for nested in descriptor.nested_type]
        )

    if isinstance(descriptor, FileDescriptorProto):
        return len(descriptor.enum_type) + sum(
            [count_enums(nested) for nested in descriptor.message_type]
        )

    raise TypeError("Only file and message descriptors are supported.")


def count_services(descriptor: FileDescriptorProto) -> int:
    return len(descriptor.service)


def count_methods(
    descriptor: Union[FileDescriptorProto, ServiceDescriptorProto]
) -> int:
    if isinstance(descriptor, FileDescriptorProto):
        return sum([count_methods(nested) for nested in descriptor.service])

    if isinstance(descriptor, ServiceDescriptorProto):
        return len(descriptor.method)

    raise TypeError("Only file and service descriptors are supported.")
