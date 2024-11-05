import os


def generate_structure(root_dir, output_file, exclude_dirs=None):
    if exclude_dirs is None:
        exclude_dirs = []

    def print_tree(dir_path, prefix="", file=None):
        contents = [d for d in os.listdir(dir_path) if d not in exclude_dirs]
        folders = sorted(
            [c for c in contents if os.path.isdir(os.path.join(dir_path, c))]
        )
        files = sorted(
            [c for c in contents if os.path.isfile(os.path.join(dir_path, c))]
        )

        sorted_contents = folders + files
        pointers = ["├── "] * (len(sorted_contents) - 1) + ["└── "]

        for pointer, name in zip(pointers, sorted_contents):
            path = os.path.join(dir_path, name)
            if os.path.isdir(path):
                file.write(f"{prefix}{pointer}{name}/\n")
                extension = "│   " if pointer == "├── " else "    "
                print_tree(path, prefix + extension, file)
            else:
                file.write(f"{prefix}{pointer}{name}\n")

    repo_name = os.path.basename(os.path.abspath(root_dir))

    with open(output_file, "w") as f:
        f.write("```\n")
        f.write(f"{repo_name}/\n")
        print_tree(root_dir, "", f)
        f.write("```\n")


if __name__ == "__main__":
    generate_structure(
        ".",
        "structure.md",
        exclude_dirs=[".git", "__pycache__", "venv", ".ruff_cache"],
    )
