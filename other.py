#!/usr/bin/env python3
import logging
import math
import string
import sys
import random

from bs4 import BeautifulSoup as bs
from google.protobuf.compiler.plugin_pb2 import CodeGeneratorResponse, CodeGeneratorRequest
from google.protobuf.descriptor_pb2 import FieldDescriptorProto, DescriptorProto

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

def get_field_value(field):
    if field.type == FieldDescriptorProto.Type.TYPE_STRING:
        return "\"" + ''.join(random.choice(string.ascii_letters) for _ in range(10)) + "\""
    if field.type == FieldDescriptorProto.Type.TYPE_BOOL:
        return random.choice(["True", "False"])
    if field.type == FieldDescriptorProto.Type.TYPE_UINT32:
        return abs(random.randint(0, 4_294_967_295))
    if field.type == FieldDescriptorProto.Type.TYPE_INT32:
        return abs(random.randint(-2_147_483_648, 2_147_483_648))
    if field.type == FieldDescriptorProto.Type.TYPE_UINT64:
        return abs(random.randint(0, 4_294_967_295))
    if field.type == FieldDescriptorProto.Type.TYPE_INT64:
        return abs(random.randint(-9_223_372_036_854_775_808, 9_223_372_036_854_775_808))
    if field.type == FieldDescriptorProto.Type.TYPE_ENUM:
        return "enum-value"

    else:
        raise NotImplementedError(f"{FieldDescriptorProto.Type.Name(field.type)} not implemented")


def get_message_field_code(name, field):
    return f"{name}.{field.name} = {get_field_value(field)}"




def message_generator(proto_name, message):
    name = message.name
    name = name[0].lower() + name[1:]
    code = [f"""{name} = {proto_name}.{message.name}()"""]
    for field in message.field:
        code.append(get_message_field_code(name, field))

    logger.info(code)
    return "\n".join(code)

def get_message_html(proto_name,message):
    logger.info(f"Generating code for {message.name}")
    # logger.info(f"Location: {message}")
    code = message_generator(proto_name, message).replace("\n", "<br>\n")
    r = \
        f"""
        <h2>{message.name}</h2>
        <p style="background-color:lightgray;padding=.5">
        <code >
        {code}
        </code>
        </p>
         """
    return r


def generateCode(request: CodeGeneratorRequest) -> CodeGeneratorResponse:
    response = CodeGeneratorResponse()
    for proto_file in request.proto_file:
        logger.info(f"Generating code for {proto_file.name}")
        file = response.file.add()
        file.name = proto_file.name.replace(".proto", "_doc.html")
        content = f"<h1>{proto_file.name}</h1>" \
                  + "\n".join([get_message_html(proto_file.name.replace(".proto", "_pb2"), m) for m in proto_file.message_type])
        logger.info("Prettifying content")
        file.content = bs(content, features="html.parser").prettify()
    return response


if __name__ == "__main__":
    data = sys.stdin.buffer.read()
    request = CodeGeneratorRequest.FromString(data)
    logger.info(request)
    response = generateCode(request)
    sys.stdout.buffer.write(response.SerializeToString())
