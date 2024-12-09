import os
from pathlib import Path
import shutil

from document import generate_pages_recursively


def main():
    # Assumes file is '.../src/main.py' and gets to base directory '.../'
    root = Path(__file__).parent.parent
    recursive_copy(root / "static", root / "public")
    generate_pages_recursively(
        root / "content",
        root / "template.html",
        root / "public",
    )


def recursive_copy(source: Path, target: Path) -> None:
    clear_directory(target)

    items = source.iterdir()
    for item in items:
        dest = target / item.name
        if item.is_dir():
            recursive_copy(item, dest)
        else:
            shutil.copy(item, dest)


def clear_directory(dir):
    try:
        shutil.rmtree(dir)
    except FileNotFoundError:
        pass
    except NotADirectoryError:
        print(f"Aborting: {dir} is not a directory")
        exit(1)
    except PermissionError:
        print(f"Aborting: restricted access to {dir}")
        exit(1)

    try:
        os.mkdir(dir)
    except FileExistsError:
        print(f"Aborting: destination was deleted but still exists")
        exit(1)
    except PermissionError as e:
        print(f"Aborting: {e}")
        exit(1)
    except FileNotFoundError as e:
        print(f"Aborting: {e}")
        exit(1)
    except OSError as e:
        print(f"Aborting: OS error {e}")
        exit(1)
    except Exception as e:
        print(e)
        exit(1)


if __name__ == "__main__":
    main()
