# -*- coding: utf-8 -*-
"""AI 시대, 우리 아이의 미래를 준비하는 부모 교육 — 슬라이드 생성.

슬라이드 순서가 바뀌어도 쪽번호와 본문·노트의 상호 참조가 어긋나지 않도록,
참조는 {이름} 토큰으로 쓰고 조립이 끝난 뒤 실제 번호로 바꿔 넣는다.
"""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deckkit import new_deck
import slides_a as A, slides_b as B, slides_c as C, slides_d as D

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "AI시대_학부모연수_20260917.pptx")

# (참조 이름, 슬라이드 함수) — 이 목록의 순서가 곧 발표 순서다.
ORDER = [
    ("cover",      A.s01), ("worry",     A.s02), ("three",     A.s03), ("ox",       A.s04),
    ("how",        A.s05), ("fork",      A.s06), ("readres",   A.s07), ("bastani",  A.s08),
    ("debt",    D.d_cogdebt),
    ("age",        A.s09), ("ready",     A.s10),
    ("school",     B.s11), ("checklist", B.s12), ("account",   B.s13), ("compare", B.s13a),
    ("familylink", B.s14a),
    ("together", D.d_together),
    ("signal",     B.s14), ("order",     B.s15), ("tools3",    B.s16),
    ("paper",   D.d_paper), ("pisa",  D.d_pisa),
    ("homework",   B.s17), ("levels",    B.s18),
    ("tasktypes", D.d_homework),
    ("quiz",       B.s19), ("prompt",    B.s20), ("formula",   C.s21),
    ("overdep", D.d_overdep),
    ("habit",      C.s22), ("factcheck", C.s23), ("detective", C.s24), ("privacy",  C.s25),
    ("thai",    D.d_thailand), ("aigood", D.d_aiforgood), ("nobel", D.d_nobel),
    ("bok",     D.d_bok), ("myth", D.d_myth), ("wef", D.d_wef),
    ("tower",      C.s26),
    ("five",    D.d_five),
    ("trouble",    C.s27), ("promise",   C.s28), ("summary",   C.s29), ("closing", C.s30),
]

PAGENUM = re.compile(r"^\s*\d+\s*/\s*\d+\s*$")
TOKEN = re.compile(r"\{([a-z0-9_]+)\}")


def finalize(prs, keymap):
    """쪽번호를 다시 찍고, 본문·노트의 {이름} 토큰을 실제 장 번호로 바꾼다."""
    slides = list(prs.slides)
    total = len(slides)
    stamped = 0
    unknown = set()

    def sub(run):
        if "{" not in run.text:
            return
        def rep(m):
            k = m.group(1)
            if k not in keymap:
                unknown.add(k)
                return m.group(0)
            return str(keymap[k])
        run.text = TOKEN.sub(rep, run.text)

    for i, s in enumerate(slides, 1):
        done = False
        for sh in s.shapes:
            if not sh.has_text_frame:
                continue
            if not done and PAGENUM.match(sh.text_frame.text):
                runs = [r for p in sh.text_frame.paragraphs for r in p.runs]
                if runs:
                    runs[0].text = f"{i} / {total}"
                    for r in runs[1:]:
                        r.text = ""
                    stamped += 1
                    done = True
                    continue
            for p in sh.text_frame.paragraphs:
                for r in p.runs:
                    sub(r)
        if s.has_notes_slide:
            for p in s.notes_slide.notes_text_frame.paragraphs:
                for r in p.runs:
                    sub(r)
    return total, stamped, unknown


def main():
    prs = new_deck()
    keymap = {name: i for i, (name, _) in enumerate(ORDER, 1)}
    for _, fn in ORDER:
        fn(prs)
    total, stamped, unknown = finalize(prs, keymap)
    core = prs.core_properties
    core.title = "AI 시대, 우리 아이의 미래를 준비하는 부모 교육"
    core.subject = "학부모 연수 (2026. 9. 17.)"
    core.comments = ("학교의 AI 교육부터 가정에서 실천하는 올바른 AI 활용법까지. "
                     "슬라이드 하단 출처는 눌러서 원문으로 이동하며, 연구 조건·해석의 한계·"
                     "퀴즈 정답은 발표자 노트에 수록.")
    prs.save(OUT)
    print(f"저장: {OUT}")
    print(f"슬라이드 {total}장 · 쪽번호 {stamped}장 표기")
    if unknown:
        print(f"!! 알 수 없는 참조 이름: {sorted(unknown)}")


if __name__ == "__main__":
    main()
