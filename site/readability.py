"""Readability of the site's own prose, tab by tab.
Flesch Reading Ease and Flesch-Kincaid grade with a rule-based English syllable
counter (no dictionary download needed). Figures, tables, scripts and citation
years are excluded. Run: python3 readability.py [index.html]"""
import re, sys, html

def syllables(word):
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w: return 0
    if len(w) <= 3: return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    groups = re.findall(r"[aeiouy]+", w)
    return max(1, len(groups))

def prose(section_html):
    s = re.sub(r"<figure.*?</figure>", "", section_html, flags=re.S)
    s = re.sub(r"<table.*?</table>", "", s, flags=re.S)
    s = re.sub(r"<(script|style).*?</\1>", "", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"\([^)]*\d{4}[^)]*\)", "", s)          # citation parentheticals
    s = re.sub(r"\b[A-Z][A-Za-z]+ \d+\([\d)]+", "", s)  # journal volume/issue
    return re.sub(r"\s+", " ", s).strip()

def scores(text):
    sents = [x for x in re.split(r"(?<=[.!?])\s+", text) if re.search(r"[a-zA-Z]", x)]
    words = re.findall(r"[A-Za-z][A-Za-z'’-]*", text)
    syl = sum(syllables(w) for w in words)
    W, S = max(1, len(words)), max(1, len(sents))
    ease = 206.835 - 1.015 * (W / S) - 84.6 * (syl / W)
    grade = 0.39 * (W / S) + 11.8 * (syl / W) - 15.59
    return {"words": W, "sentences": S, "wps": W / S, "ease": ease, "grade": grade}

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "index.html"
    src = open(path, encoding="utf-8").read()
    secs = re.findall(r'<section role="tabpanel" id="(\w+)"(.*?)</section>', src, re.S)
    rows, alltext = [], []
    for sid, body in secs:
        t = prose(body); alltext.append(t); r = scores(t); rows.append((sid, r))
    rows.append(("whole site", scores(" ".join(alltext))))
    print(f"{'tab':12s} {'words':>6s} {'w/sent':>7s} {'ease':>6s} {'grade':>6s}")
    for sid, r in rows:
        print(f"{sid:12s} {r['words']:6d} {r['wps']:7.1f} {r['ease']:6.1f} {r['grade']:6.1f}")
