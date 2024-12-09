from pathlib import Path

from block import markdown_to_html_node


def extract_title(markdown: str):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()

    raise Exception("Document has no h1 header")


def generate_page(from_path: Path, template_path: Path, dest_path: Path) -> None:
    print(
        "Generating page:\n"
        f"  From:  {from_path}\n"
        f"  To:    {dest_path}\n"
        f"  Using: {template_path}"
    )
    with open(from_path) as markdown_file:
        markdown = markdown_file.read()
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    with open(template_path) as template_file:
        template = template_file.read()
    page = template
    page = page.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", html)

    with open(dest_path, mode="x") as dest_file:
        dest_file.write(page)