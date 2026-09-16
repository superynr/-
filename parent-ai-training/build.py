# -*- coding: utf-8 -*-
"""AI 시대, 우리 아이의 미래를 준비하는 부모 교육 — 슬라이드 생성."""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deckkit import new_deck
import slides_a, slides_b, slides_c, slides_d

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "AI시대_학부모연수_20260917.pptx")
A, B, C, D = slides_a, slides_b, slides_c, slides_d


def order():
    return ([getattr(A, f"s{i:02d}") for i in range(1, 11)] +
            [B.s11, B.s12, B.s13, B.s13a, B.s14a, B.s14, B.s15, B.s16] +
            [D.d_paper, D.d_pisa] +
            [B.s17, B.s18, B.s19, B.s20, C.s21] +
            [D.d_overdep] +
            [C.s22, C.s23, C.s24, C.s25] +
            [D.d_thailand, D.d_aiforgood, D.d_nobel, D.d_bok, D.d_myth, D.d_wef] +
            [C.s26, C.s27, C.s28, C.s29, C.s30])


def stamp_pages(prs):
    """조립이 끝난 뒤 쪽번호를 순서대로 다시 찍는다."""
    slides = list(prs.slides)
    total = len(slides)
    pat = re.compile(r"^\s*\d+\s*/\s*\d+\s*$")
    stamped = 0
    for i, s in enumerate(slides, 1):
        for sh in s.shapes:
            if not sh.has_text_frame:
                continue
            if pat.match(sh.text_frame.text):
                runs = [r for p in sh.text_frame.paragraphs for r in p.runs]
                if runs:
                    runs[0].text = f"{i} / {total}"
                    for r in runs[1:]:
                        r.text = ""
                    stamped += 1
                break
    return total, stamped


def main():
    prs = new_deck()
    for fn in order():
        fn(prs)
    total, stamped = stamp_pages(prs)
    core = prs.core_properties
    core.title = "AI 시대, 우리 아이의 미래를 준비하는 부모 교육"
    core.subject = "학부모 연수 (2026. 9. 17.)"
    core.comments = ("학교의 AI 교육부터 가정에서 실천하는 올바른 AI 활용법까지. "
                     "슬라이드 하단 출처는 눌러서 원문으로 이동하며, 연구 조건·해석의 한계·"
                     "퀴즈 정답은 발표자 노트에 수록.")
    prs.save(OUT)
    print(f"저장: {OUT}")
    print(f"슬라이드 {total}장 · 쪽번호 {stamped}장에 표기")


if __name__ == "__main__":
    main()
