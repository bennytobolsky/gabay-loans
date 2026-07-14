import json
import math
import pandas as pd

SRC = "קובץ מרכז הלווואת.xlsx"
HTML = "index.html"

COLUMN_MAP = {
    "שם הגוף המלווה": "שם הגוף המלווה",
    "סוג מוצר (השתלמות/גמל/פנסיה)": "סוג מוצר",
    "סטטוס כספים (נזיל / לא נזיל)": "סטטוס",
    "מסלול השקעה (שם המסלול / כל המסלולים)": "מסלול",
    "שיעור הלוואה מקסימלי (%)": "שיעור הלוואה מקסימלי (%)",
    "ריבית (נוסחה או אחוז קבוע)": "ריבית",
    "סוגי החזר אפשריים (שפיצר/בלון/גרייס)": "סוגי החזר",
    "תקופת הלוואה בשנים": "תקופה",
    "סכום מינימום להלוואה (₪)": "מינימום",
    "סכום מקסימום להלוואה (₪)": "מקסימום",
    "הערות מיוחדות / חריגים": "הערות",
}


def clean(v):
    if v is None:
        return None
    if isinstance(v, float) and math.isnan(v):
        return None
    if isinstance(v, str):
        s = v.strip()
        return s if s else None
    return v


def build_records():
    df = pd.read_excel(SRC)
    df = df.rename(columns=COLUMN_MAP)
    records = []
    for _, row in df.iterrows():
        rec = {}
        for key in COLUMN_MAP.values():
            val = clean(row.get(key))
            if val is not None:
                rec[key] = val
        records.append(rec)
    return records


def main():
    records = build_records()
    data_json = json.dumps(records, ensure_ascii=False, separators=(",", ":"))

    html = open(HTML, encoding="utf-8").read()
    start_marker = "const DATA = ["
    start = html.index(start_marker)
    end = html.index("];", start) + 2
    new_line = "const DATA = " + data_json + ";"
    html = html[:start] + new_line + html[end:]
    open(HTML, "w", encoding="utf-8").write(html)

    companies = sorted({r["שם הגוף המלווה"] for r in records})
    print(f"עודכן {HTML} עם {len(records)} שורות מתוך {SRC}")
    print("חברות בנתונים:", ", ".join(companies))
    print("תזכורת: לוודא שכפתורי סינון החברה בסרגל הצד ב-index.html עדיין תואמים לרשימה הזו.")


if __name__ == "__main__":
    main()
