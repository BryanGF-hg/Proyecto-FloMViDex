import json
from typing import Any, Dict, List

def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def compare_values(path: str, v1: Any, v2: Any, diffs: Dict[str, List]):
    """Compara dos valores simples y registra diferencias."""
    if v1 != v2:
        diffs["changed"].append({
            "path": path,
            "from": v1,
            "to": v2
        })

def compare_json(obj1: Any, obj2: Any, path: str = "") -> Dict[str, List]:
    """
    Compara dos objetos JSON (dict, list, valores simples).
    Devuelve un dict con listas de:
      - added: cosas solo en obj2
      - removed: cosas solo en obj1
      - changed: mismo sitio, distinto valor
    """
    diffs = {
        "added": [],
        "removed": [],
        "changed": []
    }

    # Caso diccionario
    if isinstance(obj1, dict) and isinstance(obj2, dict):
        keys1 = set(obj1.keys())
        keys2 = set(obj2.keys())

        for k in keys1 - keys2:
            diffs["removed"].append({
                "path": f"{path}.{k}" if path else k,
                "value": obj1[k]
            })

        for k in keys2 - keys1:
            diffs["added"].append({
                "path": f"{path}.{k}" if path else k,
                "value": obj2[k]
            })

        for k in keys1 & keys2:
            sub_path = f"{path}.{k}" if path else k
            sub_diffs = compare_json(obj1[k], obj2[k], sub_path)
            for key in diffs:
                diffs[key].extend(sub_diffs[key])

    # Caso lista
    elif isinstance(obj1, list) and isinstance(obj2, list):
        # Comparamos por índice
        max_len = max(len(obj1), len(obj2))
        for i in range(max_len):
            sub_path = f"{path}[{i}]"
            if i < len(obj1) and i < len(obj2):
                sub_diffs = compare_json(obj1[i], obj2[i], sub_path)
                for key in diffs:
                    diffs[key].extend(sub_diffs[key])
            elif i < len(obj1):
                diffs["removed"].append({
                    "path": sub_path,
                    "value": obj1[i]
                })
            else:
                diffs["added"].append({
                    "path": sub_path,
                    "value": obj2[i]
                })

    # Caso valor simple
    else:
        compare_values(path, obj1, obj2, diffs)

    return diffs

def save_diff(diffs: Dict[str, List], path: str = "diff.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(diffs, f, ensure_ascii=False, indent=2)
    print(f"[+] Diff guardado en {path}")

def main():
    json1 = load_json("a.json")
    json2 = load_json("b.json")

    diffs = compare_json(json1, json2)
    save_diff(diffs)

if __name__ == "__main__":
    main()
