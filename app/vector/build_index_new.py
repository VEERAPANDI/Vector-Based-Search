import os
import re
import pickle
import faiss
from sentence_transformers import SentenceTransformer

# -------------------------------
# Paths
# -------------------------------
BASE_DIR = "app/data"
COMPANY_DOC_PATH = os.path.join(BASE_DIR, "company_docs.txt")
CODE_DIR = os.path.join(BASE_DIR, "code")
DOCS_PICKLE = os.path.join(BASE_DIR, "docs.pkl")
INDEX_PATH = os.path.join(BASE_DIR, "index.faiss")

# -------------------------------
# Load embedding model
# (Works well for text + code)
# -------------------------------
model = SentenceTransformer("app/models/all-MiniLM-L6-v2")

docs = []

# =====================================================
# 1️⃣ INGEST COMPANY DOCUMENT
# =====================================================
with open(COMPANY_DOC_PATH, "r", encoding="utf-8") as f:
    text = f.read()

current_title = ""
current_content = ""

def company_priority(title: str):
    title = title.lower()
    if "service" in title or "solution" in title:
        return 5
    if "overview" in title:
        return 4
    if "contact" in title:
        return 2
    return 1

for line in text.splitlines():
    line = line.strip()
    if not line:
        continue

    if line.endswith(":") and len(line) < 60:
        if current_content:
            docs.append({
                "source": "company",
                "type": "business",
                "title": current_title.replace(":", ""),
                "priority": company_priority(current_title),
                "content": current_title + " " + current_content
            })
        current_title = line
        current_content = ""
    else:
        current_content += line + " "

if current_content:
    docs.append({
        "source": "company",
        "type": "business",
        "title": current_title.replace(":", ""),
        "priority": company_priority(current_title),
        "content": current_title + " " + current_content
    })

# =====================================================
# 2️⃣ INGEST LARAVEL FUNCTIONS (functions.php)
# =====================================================

# def extract_php_functions(code: str):
#     extracted = []

#     # Helper functions
#     helper_pattern = r"function\s+(\w+)\s*\([^)]*\)\s*(?::\s*\w+)?\s*\{[\s\S]*?\}"
#     for m in re.finditer(helper_pattern, code):
#         extracted.append({
#             "name": m.group(1),
#             "content": m.group(0),
#             "type": "helper"
#         })

#     # Controller-style methods
#     method_pattern = r"(public|protected|private)\s+function\s+(\w+)\s*\([^)]*\)\s*\{[\s\S]*?\}"
#     for m in re.finditer(method_pattern, code):
#         extracted.append({
#             "name": m.group(2),
#             "content": m.group(0),
#             "type": "controller_method"
#         })

#     return extracted

# for file in os.listdir(CODE_DIR):
#     if not file.endswith(".php"):
#         continue

#     file_path = os.path.join(CODE_DIR, file)
#     with open(file_path, "r", encoding="utf-8") as f:
#         php_code = f.read()

#     functions = extract_php_functions(php_code)

#     for fn in functions:
#         docs.append({
#             "source": "code",
#             "framework": "laravel",
#             "type": fn["type"],
#             "language": "php",
#             "file": file,
#             "name": fn["name"],
#             "priority": 30 if fn["type"] == "controller_method" else 20,
#             "content": fn["content"]
#         })


def extract_php_functions(code: str):
    extracted = []

    pattern = re.compile(
        r"(public|protected|private)?\s*function\s+(\w+)\s*\([^)]*\)\s*\{",
        re.MULTILINE | re.DOTALL
    )

    for match in pattern.finditer(code):
        start = match.start()
        name = match.group(2)

        brace_count = 0
        i = match.end() - 1

        in_single_quote = False
        in_double_quote = False
        in_line_comment = False
        in_block_comment = False

        while i < len(code):
            char = code[i]
            next_char = code[i+1] if i + 1 < len(code) else ""

            # Handle comments
            if not in_single_quote and not in_double_quote:
                if not in_block_comment and char == "/" and next_char == "/":
                    in_line_comment = True
                elif not in_line_comment and char == "/" and next_char == "*":
                    in_block_comment = True
                elif in_line_comment and char == "\n":
                    in_line_comment = False
                elif in_block_comment and char == "*" and next_char == "/":
                    in_block_comment = False
                    i += 1

            # Handle strings
            if not in_line_comment and not in_block_comment:
                if char == "'" and not in_double_quote:
                    in_single_quote = not in_single_quote
                elif char == '"' and not in_single_quote:
                    in_double_quote = not in_double_quote

            # Count braces only when safe
            if not in_single_quote and not in_double_quote and not in_line_comment and not in_block_comment:
                if char == "{":
                    brace_count += 1
                elif char == "}":
                    brace_count -= 1
                    if brace_count == 0:
                        i += 1
                        break

            i += 1

        full_function = code[start:i]

        extracted.append({
            "name": name,
            "content": full_function,
            "type": "controller_method" if match.group(1) else "helper"
        })

    return extracted

for file in os.listdir(CODE_DIR):
    if not file.endswith(".php"):
        continue

    file_path = os.path.join(CODE_DIR, file)
    with open(file_path, "r", encoding="utf-8") as f:
        php_code = f.read()

    functions = extract_php_functions(php_code)

    for fn in functions:
        docs.append({
            "source": "code",
            "framework": "laravel",
            "type": fn["type"],
            "language": "php",
            "file": file,
            "name": fn["name"],
            "priority": 30 if fn["type"] == "controller_method" else 20,
            "content": fn["content"]
        })

# =====================================================
# 3️⃣ SAVE DOCS METADATA
# =====================================================
with open(DOCS_PICKLE, "wb") as f:
    pickle.dump(docs, f)

# =====================================================
# 4️⃣ BUILD FAISS INDEX
# =====================================================
texts = [d["content"] for d in docs]
embeddings = model.encode(texts, convert_to_numpy=True)

dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(embeddings)

faiss.write_index(index, INDEX_PATH)

print(f"✅ FAISS build completed")
print(f"📄 Total documents indexed: {len(docs)}")