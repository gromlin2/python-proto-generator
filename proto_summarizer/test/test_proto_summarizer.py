import subprocess
import tempfile
from pathlib import Path

import git

GIT_ROOT = git.Repo("./", search_parent_directories=True).git.rev_parse(
    "--show-toplevel"
)


def assert_file_content_equals(generated_path: Path, expected_path: Path):
    assert generated_path.is_file()
    assert expected_path.is_file()
    with open(generated_path, "r") as generated_file:
        with open(expected_path) as expected_file:
            assert generated_file.read() == expected_file.read()


def test_hello_world():
    # Create a temporary directory to hold generated code
    generator_output_dir = tempfile.mkdtemp()
    print(f"Generating code in {generator_output_dir}")

    cmd = [
        "protoc",
        f"-I{GIT_ROOT}/proto",
        f"{GIT_ROOT}/proto/hello_world.proto",
        "--python_out=" + generator_output_dir,
        "--demo_out=" + generator_output_dir,
        f"--plugin=protoc-gen-demo={GIT_ROOT}/proto_summarizer/generator.py",
    ]
    subprocess.run(cmd)

    assert_file_content_equals(
        Path(generator_output_dir, "hello_world.html"),
        Path("test/expected/hello_world.html"),
    )


def test_marsians():
    # Create a temporary directory to hold generated code
    generator_output_dir = tempfile.mkdtemp()
    print(f"Generating code in {generator_output_dir}")

    cmd = [
        "protoc",
        f"-I{GIT_ROOT}/proto",
        f"{GIT_ROOT}/proto/solar_system/mars/mars_services.proto",
        f"{GIT_ROOT}/proto/solar_system/mars/marsians.proto",
        "--python_out=" + generator_output_dir,
        "--demo_out=" + generator_output_dir,
        f"--plugin=protoc-gen-demo={GIT_ROOT}/proto_summarizer/generator.py",
    ]
    subprocess.run(cmd)

    assert_file_content_equals(
        Path(generator_output_dir, "solar_system", "mars", "marsians.html"),
        Path("test/expected/marsians.html"),
    )
    assert_file_content_equals(
        Path(generator_output_dir, "solar_system", "mars", "mars_services.html"),
        Path("test/expected/mars_services.html"),
    )
