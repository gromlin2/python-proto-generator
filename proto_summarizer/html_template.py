from textwrap import dedent
from typing import Optional
from bs4 import BeautifulSoup as bs


def pretty_path(path: str) -> str:
    """Converts a path like a/b/c into a > b > c"""
    return path.replace("/", " &gt; ")


def plural_s(count: int) -> str:
    """Returns a plural s, if required"""
    return "" if count == 1 else "s"


def zero_as_no(count: int) -> str:
    """Replaces '0' with 'NO'"""
    return "NO" if count == 0 else f"{count}"


def render(
    *,
    proto_path: str,
    syntax: str,
    package_name: Optional[str],
    dependency_count: int,
    message_count: int,
    enum_count: int,
    service_count: int,
    method_count: int,
) -> str:
    """Renders html-code for the given proto-data"""
    rendered = dedent(
        f"""
        <html>
          <head>
            <style>
                body {{
                  background-color: #161b24;
                  font-family: sans-serif;
                  color: #e9ecf2;
                  line-height: 1.6;
                }}

                h1 {{
                  color: #6ef093;
                }}

                ul {{
                  list-style-type: none;
                }}

                li {{
                  display:inline-block;
                  background-color: #57e6e6;
                  color: black;
                  border-radius: 25px;
                  width: fit-content;
                  padding: 20px;
                  margin: 10px;
                }}

                .package {{
                  color: orange;
                }}

            </style>
            <title>{pretty_path(proto_path.replace(".proto", ""))}</title>
          </head>
          <body>
            <h1>Summary of <br/> {pretty_path(proto_path)}</h1>
            Nice protobuf you defined there using {syntax} syntax. &#9989;<br />
            Its package name is <span class="package">{package_name if package_name else 'not defined, consider adding "package [name]" to your proto'}</span>.<br />
            It is importing {zero_as_no(dependency_count)} other protobuf{plural_s(dependency_count)}.<br />
            <br />
            {pretty_path(proto_path)} contains
            <ul>
              <li><span class="count">{zero_as_no(message_count)}</span> message{plural_s(message_count)}</li>
              <li><span class="count">{zero_as_no(enum_count)}</span> enum{plural_s(enum_count)}</li>
              <li><span class="count">{zero_as_no(service_count)}</span> service{plural_s(service_count)}</li>
              <li><span class="count">{zero_as_no(method_count)}</span> method{plural_s(message_count)}</li>
            </ul>
          </body>
        </html>
        """
    )

    return bs(rendered, features="html.parser").prettify(encoding="ascii")
