# -*- coding: utf-8 -*-
"""AI 시대, 우리 아이의 미래를 준비하는 부모 교육 — 30장 슬라이드 생성."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deckkit import new_deck
import slides_a, slides_b, slides_c

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "AI시대_학부모연수_20260917.pptx")

def main():
    prs = new_deck()
    fns = ([getattr(slides_a, f"s{i:02d}") for i in range(1, 11)] +
           [slides_b.s11, slides_b.s12, slides_b.s13, slides_b.s13a, slides_b.s14a] +
           [getattr(slides_b, f"s{i:02d}") for i in range(14, 21)] +
           [getattr(slides_c, f"s{i:02d}") for i in range(21, 31)])
    for fn in fns:
        fn(prs)
    core = prs.core_properties
    core.title = "AI 시대, 우리 아이의 미래를 준비하는 부모 교육"
    core.subject = "학부모 연수 (2026. 9. 17.)"
    core.comments = ("학교의 AI 교육부터 가정에서 실천하는 올바른 AI 활용법까지. "
                     "슬라이드 하단에 출처, 발표자 노트에 연구 조건·해석의 한계·퀴즈 정답 수록.")
    prs.save(OUT)
    print(f"저장: {OUT}  (슬라이드 {len(prs.slides.__iter__.__self__._sldIdLst)}장)")

if __name__ == "__main__":
    main()
