import os
from pathlib import Path
from datetime import datetime


def extract_python_files(output_filename="extracted_code.md"):
    current_dir = Path.cwd()

    script_name = Path(__file__).name
    output_path = current_dir / output_filename

    ignore_dirs = {
        ".git",
        "__pycache__",
        "venv",
        ".venv",
        "build",
        "dist",
        "env",
        ".idea",
        ".vscode",
    }

    markdown_content = []
    markdown_content.append(f"# Python Code Extraction - {current_dir.name}\n")
    markdown_content.append(
        f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    )

    py_files = []

    for root, dirs, files in os.walk(current_dir):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        for file in files:
            if file.endswith(".py") or file.endswith(".zyx"):
                if file == script_name or file == output_filename:
                    continue
                py_files.append(Path(root) / file)

    if not py_files:
        print("Không tìm thấy tệp tin Python nào khác trong thư mục hiện hành.")
        return

    for file_path in sorted(py_files, key=lambda p: p.relative_to(current_dir)):
        rel_path = file_path.relative_to(current_dir)
        markdown_content.append(f"## File: `{rel_path}`\n")
        markdown_content.append("```python\n")

        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            markdown_content.append(content)
        except Exception as e:
            markdown_content.append(f"# [Lỗi khi đọc tệp tin: {str(e)}]")

        if markdown_content and not markdown_content[-1].endswith("\n"):
            markdown_content.append("\n")
        markdown_content.append("```\n\n")

    try:
        with open(output_path, "w", encoding="utf-8") as out_f:
            out_f.write("".join(markdown_content))
        print(f"Trích xuất hoàn tất. Kết quả được lưu tại: {output_path.resolve()}")
    except Exception as e:
        print(f"Có lỗi xảy ra trong quá trình ghi tệp đầu ra: {e}")


if __name__ == "__main__":
    extract_python_files()
