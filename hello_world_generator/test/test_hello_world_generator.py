import subprocess
import tempfile
from pathlib import Path


def test_hello_world():
    # Create a temporary directory to hold generated code
    generator_output_dir = tempfile.mkdtemp()
    print(f"Generating code in {generator_output_dir}")

    cmd = ['protoc',
                    '-I../../proto',
                    '../../proto/hello_world.proto',
                    '--python_out=' + generator_output_dir,
                    '--hello-world_out=' + generator_output_dir,
                    '--plugin=protoc-gen-hello-world=../hello_world_generator.py']
    subprocess.run(cmd)

    generated_file = Path(generator_output_dir, "hello_world.txt")
    assert generated_file.is_file()
    with open(generated_file, 'r') as file:
        assert file.read() == "Greetings, world!"