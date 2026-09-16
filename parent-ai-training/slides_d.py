# -*- coding: utf-8 -*-
"""추가 사례 슬라이드 — 미래 직업, 연구 결과"""
from deckkit import *
from pptx.enum.text import PP_ALIGN

U_NOBEL = "https://www.nobelprize.org/prizes/physics/2024/summary/"
U_BOK = "https://www.bok.or.kr/portal/bbs/P0002353/view.do?menuNo=200433&nttId=10080538"
U_MYTH = "https://pluralist.com/future-of-work-statistic-closer-look/"
U_WEF = ("https://www.weforum.org/press/2025/01/future-of-jobs-report-2025-78-million-"
         "new-job-opportunities-by-2030-but-urgent-upskilling-needed-to-prepare-workforces/")
U_PAPER = "https://www.learntechlib.org/p/204447/"
U_PISA = "https://www.oecd.org/en/publications/pisa-2022-results-volume-i_53f23881-en.html"
U_NIA = "https://www.nia.or.kr/site/nia_kor/ex/bbs/View.do?cbIdx=65914&bcIdx=27831&parentSeq=27831"


def d_nobel(prs):
    s = blank(prs)
    y = title(s, "2024년 노벨 물리학상과 화학상, 모두 AI였습니다", kicker="미래의 직업",
              sub="과학의 최전선이 이미 바뀌었다는 신호입니다.")
    cw = (CW - 0.4) / 2
    panels = [("노벨 물리학상", "존 홉필드 · 제프리 힌턴",
               ["인공신경망의 기초를 세운 공로.",
                "지금의 AI가 작동하는 원리를",
                "1980년대에 만들어 두었습니다."], "blue", "tintblue"),
              ("노벨 화학상", "데이비드 베이커 · 데미스 허사비스 · 존 점퍼",
               ["AI로 단백질 구조를 예측하고",
                "설계한 공로. 50년 묵은 난제를",
                "‘알파폴드’가 풀었습니다."], "teal", "tintteal")]
    for i, (prize, who, body, col, bg) in enumerate(panels):
        x = ML + i * (cw + 0.4)
        rrect(s, x, y + 0.3, cw, 2.55, fill=bg, line=None, radius=0.1)
        rect(s, x + 0.35, y + 0.6, 0.45, 0.05, fill=col)
        txt(s, x + 0.35, y + 0.82, cw - 0.7, 0.4, prize, size=19, bold=True, color=col)
        txt(s, x + 0.35, y + 1.32, cw - 0.7, 0.4, who, size=14, bold=True, color="ink")
        txt(s, x + 0.35, y + 1.82, cw - 0.7, 0.9, body, size=13.5, color="body", spacing=1.35)
    rrect(s, ML, y + 3.1, CW, 1.15, fill="ink", line=None, radius=0.1)
    txt(s, ML + 0.4, y + 3.32, CW - 0.8, 0.75,
        ["다섯 분 모두 ‘컴퓨터를 잘 다뤄서’ 받은 상이 아닙니다.",
         "물리학자는 물리학 문제를, 생물학자는 단백질 문제를 AI로 풀어서 받았습니다."],
        size=15, bold=True, color="white", spacing=1.4)
    footer(s, 0, "출처: 노벨재단, 2024년 노벨 물리학상·화학상 수상자 발표", link=U_NOBEL)
    notes(s, "미래 직업 이야기를 여는 장입니다. 학부모의 관심이 가장 크게 움직이는 지점이기도 합니다.\n"
             "2024년 노벨 물리학상은 인공신경망의 기초를 세운 존 홉필드와 제프리 힌턴에게, "
             "화학상은 AI로 단백질 구조를 예측·설계한 데이비드 베이커, 데미스 허사비스, 존 점퍼에게 "
             "돌아갔습니다. 한 해에 두 개 분야의 노벨상이 AI 관련 연구에 간 것은 처음입니다.\n"
             "가장 중요한 해석은 아래 띠입니다. 이분들은 ‘AI 전공자’여서가 아니라 자기 분야의 오래된 문제를 "
             "AI라는 도구로 풀어서 상을 받았습니다. 아이에게 필요한 것도 ‘AI를 다루는 법’이 아니라 "
             "‘풀고 싶은 문제’와 ‘그 분야의 실력’이라는 점으로 이어 주십시오.\n"
             "코딩 학원을 보내야 하느냐는 질문이 나오면 이 장으로 답하시면 됩니다.")
    return s


def d_bok(prs):
    s = blank(prs)
    y = title(s, "그럼 어떤 직업이 안전할까요?", kicker="미래의 직업",
              sub="한국은행이 국내 취업자를 분석한 결과는 예상과 반대였습니다.")
    # 왼쪽: 핵심 수치
    rrect(s, ML, y + 0.3, 3.5, 2.45, fill="tintblue", line=None, radius=0.1)
    txt(s, ML + 0.35, y + 0.62, 2.8, 0.6, "341만 명", size=38, bold=True, color="blue")
    txt(s, ML + 0.35, y + 1.42, 2.8, 0.6,
        ["AI로 대체될 가능성이", "높은 국내 일자리"], size=14, color="body", spacing=1.3)
    rect(s, ML + 0.35, y + 2.12, 2.8, 0.012, fill="line")
    txt(s, ML + 0.35, y + 2.28, 2.8, 0.3, "전체 취업자의 12%", size=14, bold=True, color="ink")

    # 오른쪽: AI 노출 지수 순위 (단일 계열, 0~100% 전체 축)
    cx, tw = 7.05, 4.35
    txt(s, ML + 3.9, y + 0.3, 7.6, 0.3, "AI 노출 지수가 높은 직업 — 전체 직업 중 순위",
        size=13, bold=True, color="teal")
    jobs = [("일반 의사 · 한의사", 1), ("전문 의사", 7), ("회계사", 19),
            ("자산운용가", 19), ("변호사", 21)]
    for i, (name, pct) in enumerate(jobs):
        ry = y + 0.82 + i * 0.4
        txt(s, ML + 3.9, ry - 0.02, 2.95, 0.3, name, size=12.5, color="ink")
        rect(s, cx, ry + 0.1, tw, 0.035, fill="line")
        mx = cx + tw * pct / 100.0
        oval(s, mx - 0.08, ry + 0.035, 0.16, 0.16, fill="blue")
        txt(s, mx + 0.16, ry - 0.01, 1.4, 0.3, f"상위 {pct}%", size=12, bold=True, color="blue")
    ay = y + 2.86
    rect(s, cx, ay, tw, 0.012, fill="line")
    for lab, fx in (("0%", 0.0), ("50%", 0.5), ("100%", 1.0)):
        txt(s, cx + tw * fx - 0.3, ay + 0.08, 0.6, 0.25, lab, size=10,
            color="mute", align=PP_ALIGN.CENTER)
    txt(s, cx, ay + 0.34, 2.2, 0.25, "← 노출 높음", size=10.5, color="mute")
    txt(s, cx + tw - 2.2, ay + 0.34, 2.2, 0.25, "노출 낮음 →", size=10.5,
        color="mute", align=PP_ALIGN.RIGHT)

    rrect(s, ML, y + 3.55, CW, 1.05, fill="tintteal", line=None, radius=0.1)
    rich(s, ML + 0.4, y + 3.76, CW - 0.8, 0.7,
         [[("안전하다고 여겨지던 전문직일수록 오히려 위쪽에 있습니다.", "teal", True)],
          [("기존 기술과 달리 AI는 고소득·고학력 일자리에 더 많이 닿는 것으로 분석되었습니다.",
            "body", False)]],
         size=14.5, spacing=1.35, space_after=4)
    footer(s, 0, "출처: 한국은행 BOK 이슈노트 제2023-30호 「AI와 노동시장 변화」", link=U_BOK)
    notes(s, "학부모가 가장 놀라는 장입니다. 천천히 읽어 주세요.\n"
             "한국은행이 AI 특허 정보를 이용해 직업별 ‘AI 노출 지수’를 계산한 결과, 국내 취업자 약 341만 명"
             "(전체의 12%)이 AI로 대체될 가능성이 높은 것으로 나타났습니다.\n"
             "노출 지수가 높은 직업으로 일반 의사와 한의사가 상위 1% 이내, 전문 의사 7%, 회계사와 "
             "자산운용가 19%, 변호사 21%로 보고되었습니다. 그래프에서 점이 모두 왼쪽 끝에 몰려 있는 것이 "
             "이 이야기의 핵심입니다.\n"
             "해석의 주의: ①‘대체 가능성이 높다’는 것이 ‘그 직업이 없어진다’는 뜻은 아닙니다. 업무의 일부가 "
             "바뀐다는 의미로 읽어야 합니다. ②2023년 분석이고 기술 변화가 빠른 분야입니다. "
             "③특정 직업을 폄하하는 자리가 아니라, ‘안전한 직업을 찍어 주는 방식’이 잘 통하지 않는다는 "
             "점을 보여 주는 자료입니다. 이 단서를 꼭 함께 말해 주십시오.")
    return s


def d_myth(prs):
    s = blank(prs)
    y = title(s, "이 문장, 어디선가 들어보셨을 겁니다", kicker="자료 읽는 법",
              sub="미래 직업 이야기에 거의 빠지지 않고 나오는 수치입니다.")
    rrect(s, ML, y + 0.28, CW, 1.05, fill="tint", line="line", radius=0.1)
    rect(s, ML + 0.4, y + 0.5, 0.05, 0.62, fill="mute")
    txt(s, ML + 0.7, y + 0.52, CW - 1.3, 0.6,
        "“지금 초등학교에 입학하는 아이의 65%는, 지금은 없는 직업을 갖게 됩니다.”",
        size=18, color="ink")
    cards = [("2016년 보고서에 실렸습니다", "세계경제포럼의 『직업의 미래』\n보고서에 등장했습니다."),
             ("직접 조사한 것이 아닙니다", "‘널리 인용되는 추정치’라고\n소개되었을 뿐입니다."),
             ("원 연구를 찾지 못했습니다", "교육 연구자들이 출처를\n추적했지만 확인하지 못했습니다.")]
    cw, gap = 3.6, 0.42
    for i, (h, b) in enumerate(cards):
        x = ML + i * (cw + gap)
        rrect(s, x, y + 1.58, cw, 1.72, fill="tint", line="line", radius=0.1)
        numbadge(s, x + 0.32, y + 1.82, 0.4, i + 1, fill="mute", size=13)
        txt(s, x + 0.32, y + 2.34, cw - 0.64, 0.4, h, size=15, bold=True, color="ink", spacing=1.15)
        txt(s, x + 0.32, y + 2.76, cw - 0.64, 0.6, b.split("\n"), size=12.5,
            color="body", spacing=1.3)
    rrect(s, ML, y + 3.58, CW, 1.05, fill="tintteal", line=None, radius=0.1)
    rich(s, ML + 0.4, y + 3.79, CW - 0.8, 0.7,
         [[("그래서 오늘 이 연수에서는 이 수치를 쓰지 않았습니다.", "teal", True)],
          [("그럴듯하고 자주 인용될수록 출처를 봐야 합니다. 앞서 본 세 가지 질문이 이럴 때 쓰입니다.",
            "body", False)]],
         size=14.5, spacing=1.35, space_after=4)
    footer(s, 0, "출처: 2016년 세계경제포럼 보고서에 인용된 추정치 · 근거 추적 관련 논의",
           link=U_MYTH)
    notes(s, "이 장은 오늘 연수에서 가장 정직한 장입니다. 다른 학부모 연수에서 이 수치를 들은 분도 계실 겁니다.\n"
             "설명 순서: 먼저 문장을 읽어 주고 ‘들어보신 분?’ 하고 손을 들게 합니다. 그다음 세 카드를 넘기며 "
             "이 수치의 출처가 확인되지 않는다는 점을 전합니다.\n"
             "주의: ‘거짓말이다’라고 단정하지는 마십시오. 정확한 표현은 ‘근거가 되는 원 연구를 확인할 수 "
             "없다’입니다. 미래에 새로운 직업이 생긴다는 방향 자체가 틀렸다는 뜻도 아닙니다. "
             "숫자의 정확성과 방향의 타당성은 다른 문제라고 정리해 주세요.\n"
             "{detective}장 ‘사실 확인 탐정’ 활동과 연결됩니다. 아이에게 가르치려는 습관을 어른이 먼저 쓴 사례라고 "
             "말씀하시면 설득력이 큽니다.")
    return s


def d_wef(prs):
    s = blank(prs)
    y = title(s, "우리 아이가 무엇이 될지는 아무도 모릅니다", kicker="미래의 직업",
              sub="세계경제포럼이 2030년까지로 내다본 변화입니다.")
    stats = [("1억 7천만 개", "새로 생기는 일자리", "blue", "tintblue"),
             ("9,200만 개", "사라지는 일자리", "ink", "tint"),
             ("22%", "일자리 지형이\n바뀌는 비율", "teal", "tintteal"),
             ("40%", "직무에 필요한 기술 중\n바뀌는 비율", "teal", "tintteal")]
    cw = (CW - 3 * 0.3) / 4
    for i, (big, lab, col, bg) in enumerate(stats):
        x = ML + i * (cw + 0.3)
        rrect(s, x, y + 0.3, cw, 2.25, fill=bg, line=None if bg != "tint" else "line", radius=0.1)
        txt(s, x + 0.2, y + 0.72, cw - 0.4, 0.6, big, size=27, bold=True, color=col,
            align=PP_ALIGN.CENTER)
        txt(s, x + 0.2, y + 1.52, cw - 0.4, 0.7, lab.split("\n"), size=13.5, color="body",
            align=PP_ALIGN.CENTER, spacing=1.3)
    rrect(s, ML, y + 2.85, CW, 1.6, fill="ink", line=None, radius=0.1)
    txt(s, ML + 0.5, y + 3.1, CW - 1.0, 0.5,
        "직업을 정해 주는 대신, 바뀌는 환경에 적응할 힘을 길러 주는 편이 안전합니다.",
        size=17, bold=True, color="white")
    txt(s, ML + 0.5, y + 3.72, CW - 1.0, 0.55,
        ["오늘 배운 것이 10년 뒤에도 쓰일지는 모릅니다. 그러나 ‘모르는 것을 스스로 알아내는 방법’은",
         "직업이 바뀌어도 그대로 쓰입니다. 다음 장에 무엇부터 가르칠지 정리했습니다."],
        size=13.5, color="white", spacing=1.4)
    footer(s, 0, "출처: World Economic Forum, The Future of Jobs Report 2025", link=U_WEF)
    notes(s, "미래 직업 묶음(노벨상 → 한국은행 → 65% → 이 장)의 결론입니다.\n"
             "세계경제포럼은 2030년까지 1억 7천만 개의 일자리가 새로 생기고 9,200만 개가 사라져 "
             "순증 7,800만 개가 될 것으로 전망했습니다. 전체 일자리의 22%가 지형이 바뀌고, "
             "직무에 필요한 기술의 약 40%가 달라질 것으로 보았습니다.\n"
             "숫자를 다 외우게 하려는 장이 아닙니다. ‘없어진다’보다 ‘바뀐다’가 크다는 점, 그리고 "
             "필요한 기술이 절반 가까이 바뀐다는 점 두 가지만 남기면 충분합니다.\n"
             "해석의 주의: 전 세계 기업 대상 설문에 기반한 전망치입니다. 한국의 개별 직업에 그대로 "
             "적용되는 숫자가 아니라는 점을 한마디 덧붙여 주십시오.\n"
             "바로 다음 장에서 ‘그럼 무엇부터 가르치나’에 답합니다. 두 장을 붙여서 진행해 주세요.")
    return s


def d_paper(prs):
    s = blank(prs)
    y = title(s, "같은 글도 종이로 읽을 때 더 잘 이해합니다", kicker="연구 사례",
              sub="2000년부터 2017년까지의 연구를 모아 분석한 결과입니다.")
    cw = (CW - 0.4) / 2
    rrect(s, ML, y + 0.3, cw, 1.85, fill="tintblue", line=None, radius=0.1)
    txt(s, ML + 0.35, y + 0.58, cw - 0.7, 0.4, "종이로 읽기", size=19, bold=True, color="blue")
    txt(s, ML + 0.35, y + 1.12, cw - 0.7, 0.7,
        ["같은 글을 읽어도", "이해도 점수가 더 높았습니다."], size=14, color="body", spacing=1.35)
    rrect(s, ML + cw + 0.4, y + 0.3, cw, 1.85, fill="tint", line="line", radius=0.1)
    txt(s, ML + cw + 0.75, y + 0.58, cw - 0.7, 0.4, "화면으로 읽기", size=19, bold=True, color="mute")
    txt(s, ML + cw + 0.75, y + 1.12, cw - 0.7, 0.7,
        ["읽는 속도는 비슷했지만", "남는 것이 적었습니다."], size=14, color="body", spacing=1.35)
    rrect(s, ML, y + 2.35, CW, 1.0, fill="tint", line="line", radius=0.1)
    txt(s, ML + 0.4, y + 2.56, CW - 0.8, 0.6,
        ["연구 설계가 어떻든 결과는 같은 방향이었습니다. 종이로 읽은 쪽의 학습 효과가 컸습니다.",
         "익숙해지면 나아질 것이라는 기대와는 다른 결과입니다."],
        size=14, color="body", spacing=1.4)
    rrect(s, ML, y + 3.55, CW, 1.05, fill="tintteal", line=None, radius=0.1)
    rich(s, ML + 0.4, y + 3.76, CW - 0.8, 0.7,
         [[("화면을 없애자는 이야기가 아닙니다.", "teal", True)],
          [("긴 글과 교과서는 종이로 읽는 자리를 남겨 두자는 뜻입니다. 앞 장의 ‘책’이 그 자리입니다.",
            "body", False)]],
         size=14.5, spacing=1.35, space_after=4)
    footer(s, 0, "출처: Delgado, P., Vargas, C., Ackerman, R., & Salmerón, L. (2018). "
                 "Educational Research Review, 25, 23–38.", link=U_PAPER)
    notes(s, "앞 장에서 ‘책은 맥락을 읽는다’고 했던 것의 근거입니다.\n"
             "이 메타분석은 2000~2017년에 발표된 연구들을 모아, 같은 글을 종이와 디지털 기기로 읽었을 때를 "
             "비교했습니다. 연구 설계와 관계없이 종이로 읽을 때 학습 효과가 더 컸습니다. "
             "논문 제목이 ‘Don’t throw away your printed books(인쇄된 책을 버리지 마세요)’입니다.\n"
             "해석의 주의: ①대부분 성인·청소년 대상 연구이므로 초등학생에게 그대로 적용하기는 어렵습니다. "
             "②디지털 읽기가 쓸모없다는 뜻이 아니라, 깊이 읽어야 하는 글에서 차이가 난다는 뜻입니다. "
             "③2017년까지의 연구라는 점도 함께 말해 주십시오.\n"
             "가정에서 할 일 한 가지로 정리하면: 숙제로 읽어야 하는 긴 글은 인쇄해서 읽히거나 책으로 "
             "읽히기. 짧은 검색은 화면으로 해도 괜찮습니다.")
    return s


def d_pisa(prs):
    s = blank(prs)
    y = title(s, "기기 자체보다, 무엇에 쓰느냐가 갈랐습니다", kicker="연구 사례",
              sub="만 15세 학생을 대상으로 한 국제 학업성취도 평가 결과입니다.")
    stats = [("59%", "다른 학생의 기기 사용에\n주의가 흐트러진다고 답한 비율",
              "수학 수업에서, OECD 평균", "ink", "tint"),
             ("−15점", "매 수업 방해받는 학생의\n수학 점수",
              "연간 학습량의 약 4분의 3에 해당", "red", "redbg"),
             ("+14점", "학습 목적으로 하루 1시간\n이하 사용한 학생의 수학 점수",
              "전혀 쓰지 않은 학생과 비교", "green", "greenbg")]
    cw, gap = 3.6, 0.42
    for i, (big, lab, sub2, col, bg) in enumerate(stats):
        x = ML + i * (cw + gap)
        rrect(s, x, y + 0.3, cw, 2.6, fill=bg, line="line" if bg == "tint" else None, radius=0.1)
        txt(s, x + 0.3, y + 0.6, cw - 0.6, 0.55, big, size=30, bold=True, color=col)
        txt(s, x + 0.3, y + 1.35, cw - 0.6, 0.75, lab.split("\n"), size=13, color="ink", spacing=1.35)
        rect(s, x + 0.3, y + 2.18, cw - 0.6, 0.012, fill="line")
        txt(s, x + 0.3, y + 2.32, cw - 0.6, 0.45, sub2, size=11.5, color="mute", spacing=1.25)
    rrect(s, ML, y + 3.15, CW, 1.25, fill="tintteal", line=None, radius=0.1)
    rich(s, ML + 0.4, y + 3.37, CW - 0.8, 0.85,
         [[("다만 여가 목적으로 하루 1시간을 넘기면 점수가 크게 떨어졌습니다.", "teal", True)],
          [("같은 기기, 같은 시간이라도 학습에 썼는지 오락에 썼는지에 따라 방향이 갈렸습니다. "
            "우리 집 기준도 ‘몇 시간’보다 ‘무엇에’가 먼저입니다.", "body", False)]],
         size=14.5, spacing=1.35, space_after=4)
    footer(s, 0, "출처: OECD, PISA 2022 Results (Volume I)", link=U_PISA)
    notes(s, "‘기기를 쓰게 할까 말까’라는 이분법을 깨는 장입니다.\n"
             "PISA 2022에서 OECD 평균 59%의 학생이 수학 수업에서 다른 학생의 휴대폰·태블릿·노트북 사용 때문에 "
             "주의가 흐트러진 적이 있다고 답했습니다. 매 수업 또는 대부분의 수업에서 방해받는다고 답한 학생은 "
             "그렇지 않은 학생보다 수학 점수가 15점 낮았습니다. PISA에서 15세 학생의 연간 학습량이 약 20점이므로, "
             "15점은 약 4분의 3년치에 해당합니다.\n"
             "반대쪽 결과도 꼭 같이 전해 주세요. 학교에서 학습 목적으로 하루 1시간 이하 사용한 학생은 "
             "전혀 쓰지 않은 학생보다 14점 높았습니다. 반면 여가 목적으로 하루 1시간을 넘기면 점수가 크게 "
             "떨어졌습니다.\n"
             "해석의 주의: 만 15세 대상이고, 인과관계가 아니라 상관관계를 보여 주는 자료입니다. "
             "‘공부 잘하는 학생이 기기를 적게 쓴다’는 반대 방향의 설명도 가능하다는 점을 짚어 주시면 좋습니다.\n"
             "{signal}장 신호등의 ‘노랑’ 기준이 왜 시간이 아니라 용도인지가 여기서 설명됩니다.")
    return s


def d_overdep(prs):
    s = blank(prs)
    y = title(s, "AI 약속은 스마트폰 약속과 따로 갈 수 없습니다", kicker="사용 습관",
              sub="AI는 대부분 그 스마트폰 안에서 씁니다.")
    cw = (CW - 0.4) / 2
    rows = [("청소년", "만 10~19세", "42.6%", "+2.5%p", "blue", "tintblue"),
            ("유아동", "만 3~9세", "25.9%", "+0.9%p", "teal", "tintteal")]
    for i, (who, age, pct, delta, col, bg) in enumerate(rows):
        x = ML + i * (cw + 0.4)
        rrect(s, x, y + 0.3, cw, 2.3, fill=bg, line=None, radius=0.1)
        txt(s, x + 0.35, y + 0.58, 2.4, 0.35, who, size=18, bold=True, color="ink")
        txt(s, x + 0.35, y + 0.98, 2.4, 0.3, age, size=13, color="mute")
        txt(s, x + cw - 3.0, y + 0.62, 2.65, 0.75, pct, size=40, bold=True, color=col,
            align=PP_ALIGN.RIGHT)
        rect(s, x + 0.35, y + 1.62, cw - 0.7, 0.012, fill="line")
        txt(s, x + 0.35, y + 1.8, cw - 0.7, 0.35,
            f"스마트폰 과의존 위험군 · 전년 대비 {delta}", size=13, color="body")
    rrect(s, ML, y + 2.9, CW, 0.95, fill="tint", line="line", radius=0.1)
    txt(s, ML + 0.4, y + 3.1, CW - 0.8, 0.55,
        ["전국 1만 가구를 방문 면접해 조사한 국가승인통계입니다.",
         "두 연령대 모두 전년보다 올랐습니다."],
        size=13.5, color="body", spacing=1.4)
    rrect(s, ML, y + 4.02, CW, 0.72, fill="tintteal", line=None, radius=0.1)
    txt(s, ML + 0.4, y + 4.22, CW - 0.8, 0.4,
        "기기 사용 규칙이 없으면 AI 사용 규칙도 지켜지기 어렵습니다. 두 가지를 같이 정해 주세요.",
        size=14.5, bold=True, color="teal")
    footer(s, 0, "출처: 과학기술정보통신부·한국지능정보사회진흥원, 『2024년 스마트폰 과의존 실태조사』",
           link=U_NIA)
    notes(s, "다음 장 ‘틈만 나면 AI를 찾는 아이에게’로 넘어가기 전에 배경을 깔아 주는 장입니다.\n"
             "2024년 조사에서 청소년(만 10~19세) 42.6%, 유아동(만 3~9세) 25.9%가 스마트폰 과의존 위험군"
             "(고위험군 + 잠재적위험군)으로 나타났습니다. 두 연령대 모두 전년보다 올랐고, "
             "성인과 60대는 오히려 줄었습니다.\n"
             "‘위험군’이라는 말이 무겁게 들릴 수 있으니 설명을 덧붙여 주세요. 고위험군과 잠재적위험군을 "
             "합한 수치이며, 대부분은 잠재적위험군입니다. 진단이 아니라 조사 분류라는 점을 말해 주시면 "
             "학부모의 불안이 과해지지 않습니다.\n"
             "연결 문장: AI 사용 시간을 따로 정하려 하지 마시고, 이미 있는 스마트폰 규칙 안에 넣으시는 편이 "
             "지켜집니다. {promise}장 ‘우리 집 AI 사용 약속’을 쓸 때 이 점을 다시 짚어 주세요.")
    return s


URL_MOE_D = ("https://www.moe.go.kr/boardCnts/viewRenew.do?boardID=294"
             "&boardSeq=104984&lev=0&m=020402")
U_THAI = "https://www.bioin.or.kr/board.do?num=284299&cmd=view&bid=industry"
U_AIGOOD = "https://aiforgood.itu.int/"


def d_thailand(prs):
    s = blank(prs)
    y = title(s, "의사가 부족한 곳에서, AI가 눈을 대신 봅니다", kicker="AI가 푸는 문제",
              sub="태국의 당뇨망막병증 검진 사례입니다. 제때 발견하면 실명을 막을 수 있는 병입니다.")
    # 대비 수치
    cw = (CW - 1.4) / 2
    rrect(s, ML, y + 0.3, cw, 1.55, fill="tint", line="line", radius=0.1)
    txt(s, ML + 0.35, y + 0.55, cw - 0.7, 0.6, "약 500만 명", size=30, bold=True, color="ink")
    txt(s, ML + 0.35, y + 1.25, cw - 0.7, 0.35, "검진이 필요한 당뇨병 환자", size=14, color="body")
    txt(s, ML + cw + 0.25, y + 0.82, 0.9, 0.4, "vs", size=19, bold=True, color="mute",
        align=PP_ALIGN.CENTER)
    rrect(s, ML + cw + 1.4, y + 0.3, cw, 1.55, fill="redbg", line=None, radius=0.1)
    txt(s, ML + cw + 1.75, y + 0.55, cw - 0.7, 0.6, "약 1,400명", size=30, bold=True, color="red")
    txt(s, ML + cw + 1.75, y + 1.25, cw - 0.7, 0.35, "태국 전체의 안과 전문의", size=14, color="body")

    steps = [("눈 사진을 찍습니다", "동네 병원에서\n안저 사진 한 장"),
             ("AI가 분석합니다", "90% 이상의 정확도로\n위험을 가려냅니다"),
             ("바로 안내받습니다", "몇 주를 기다리지 않고\n치료로 이어집니다")]
    scw, gap = 3.6, 0.42
    for i, (h, b) in enumerate(steps):
        x = ML + i * (scw + gap)
        rrect(s, x, y + 2.1, scw, 1.45, fill="tintblue" if i == 2 else "tint",
              line=None if i == 2 else "line", radius=0.1)
        numbadge(s, x + 0.3, y + 2.32, 0.38, i + 1, fill="blue" if i == 2 else "teal", size=13)
        txt(s, x + 0.82, y + 2.34, scw - 1.1, 0.3, h, size=15, bold=True, color="ink")
        txt(s, x + 0.3, y + 2.78, scw - 0.6, 0.6, b.split("\n"), size=12.5,
            color="body", spacing=1.3)
    rrect(s, ML, y + 3.8, CW, 0.95, fill="tintteal", line=None, radius=0.1)
    rich(s, ML + 0.4, y + 4.0, CW - 0.8, 0.6,
         [[("기술이 앞선 나라만의 이야기가 아닙니다. ", "body", False),
           ("의사를 만나기 어려운 사람에게 먼저 닿았습니다.", "teal", True)]], size=15)
    footer(s, 0, "출처: 구글·태국 라자위티(Rajavithi)병원 당뇨망막병증 AI 검진 프로젝트", link=U_THAI)
    notes(s, "AI 이야기를 걱정으로만 듣던 학부모의 표정이 바뀌는 장입니다.\n"
             "태국에는 검진이 필요한 당뇨병 환자가 약 500만 명인데 안과 전문의는 약 1,400명뿐입니다. "
             "한 사람이 수천 명을 봐야 하는 구조라 검진을 받지 못한 채 실명하는 경우가 많았습니다. "
             "구글이 라자위티병원과 함께 안저 사진을 AI가 분석하는 검진을 도입했고, 90% 이상의 정확도로 "
             "위험군을 가려내고 있습니다.\n"
             "핵심 메시지: AI가 의사를 대신한 것이 아니라, 의사가 없는 자리를 메웠습니다. "
             "‘AI가 사람 일자리를 뺏는다’는 단순한 구도와 다른 사례라는 점을 짚어 주세요.\n"
             "해석의 주의: 실제 진료 현장에서는 사진 화질이나 인터넷 속도 때문에 어려움도 보고되었습니다. "
             "완성된 기술이라기보다 진행 중인 시도로 소개해 주십시오.\n"
             "아이에게 건넬 질문: ‘너라면 AI로 어떤 문제를 풀어 보고 싶어?’")
    return s


def d_aiforgood(prs):
    s = blank(prs)
    y = title(s, "‘AI for Good’ — 누구를 위해 쓸 것인가", kicker="AI가 푸는 문제",
              sub="2017년 국제전기통신연합(ITU)이 시작한 유엔의 플랫폼입니다. 150개국 넘게 참여합니다.")
    cases = [("홍수 예측", "강물이 넘칠 시점을 미리 알려\n대피할 시간을 법니다."),
             ("재난 조기 감지", "위성 사진의 이상을 몇 분 만에\n찾아 경보를 보냅니다."),
             ("단백질 구조 공개", "알파폴드가 밝힌 구조를\n전 세계 연구자에게 열었습니다."),
             ("질병 검진", "전문의가 부족한 지역에서\n조기 발견을 돕습니다.")]
    cw = (CW - 3 * 0.3) / 4
    for i, (h, b) in enumerate(cases):
        x = ML + i * (cw + 0.3)
        rrect(s, x, y + 0.3, cw, 2.0, fill="tintteal", line=None, radius=0.1)
        rect(s, x + 0.28, y + 0.58, 0.42, 0.05, fill="teal")
        txt(s, x + 0.28, y + 0.8, cw - 0.56, 0.4, h, size=16, bold=True, color="ink", spacing=1.15)
        txt(s, x + 0.28, y + 1.3, cw - 0.56, 0.7, b.split("\n"), size=12.5,
            color="body", spacing=1.3)
    rrect(s, ML, y + 2.55, CW, 1.05, fill="tint", line="line", radius=0.1)
    txt(s, ML + 0.4, y + 2.76, CW - 0.8, 0.65,
        ["빈곤·기아·보건·교육·환경처럼 돈이 되지 않아 미뤄지던 문제에 AI를 먼저 쓰자는 흐름입니다.",
         "기술을 얼마나 잘 만드느냐보다 ‘누구를 위해, 어떻게 쓰는가’를 묻습니다."],
        size=14, color="body", spacing=1.4)
    rrect(s, ML, y + 3.8, CW, 0.95, fill="ink", line=None, radius=0.1)
    txt(s, ML, y + 4.02, CW, 0.5,
        "집에서 아이에게 물어볼 질문도 같습니다. “이걸로 누구를 도울 수 있을까?”",
        size=17, bold=True, color="white", align=PP_ALIGN.CENTER)
    footer(s, 0, "출처: ITU(국제전기통신연합) AI for Good", link=U_AIGOOD)
    notes(s, "앞 장의 태국 사례가 하나의 예였다면, 이 장은 그런 시도가 모여 있는 흐름을 보여 줍니다.\n"
             "AI for Good은 2017년 유엔 산하 국제전기통신연합(ITU)이 시작했고, 빈곤·기아·보건·교육·환경 같은 "
             "지구적 과제에 AI를 쓰자는 플랫폼입니다. 매년 제네바에서 총회가 열리고 150개국 넘게 참여합니다.\n"
             "사례를 하나씩 짚어 주세요. 홍수 예측은 대피 시간을 벌어 주고, 위성 영상 분석은 재난을 몇 분 만에 "
             "감지합니다. 알파폴드가 밝힌 단백질 구조는 공개되어 신약 연구에 쓰이고 있습니다.\n"
             "가장 중요한 것은 맨 아래 문장입니다. 오늘 연수에서 부모가 아이에게 건넬 수 있는 가장 좋은 질문이 "
             "‘이걸로 누구를 도울 수 있을까’입니다. 성능이나 점수가 아니라 쓰임을 묻는 질문이고, "
             "이것이 {tower}장 도구 3층과 {closing}장 마무리로 이어집니다.\n"
             "시간이 부족하면 이 장은 사례 하나만 말하고 아래 문장으로 바로 넘어가셔도 됩니다.")
    return s


def d_homework(prs):
    """과제 종류별로 선 긋기 + 학원 숙제"""
    s = blank(prs)
    y = title(s, "과제 종류에 따라 선이 다릅니다", kicker="숙제와 평가",
              sub="같은 ‘숙제’라도 훈련하는 과제와 찾아보는 과제는 기준이 다릅니다.")
    tw = 8.35
    ty = y + 0.25
    rrect(s, ML, ty, tw, 3.92, fill="white", line="line", radius=0.06)
    rect(s, ML, ty, tw, 0.44, fill="tintteal")
    c1, w1, c2, w2, c3, w3 = 0.25, 1.85, 2.25, 2.95, 5.35, 2.75
    for cx, wd, hd in ((c1, w1, "구분"), (c2, w2, "이런 과제"), (c3, w3, "왜 그런가")):
        txt(s, ML + cx, ty + 0.12, wd, 0.3, hd, size=12.5, bold=True, color="teal")
    rows = [("쓰지 않기", "red", "redbg",
             ["받아쓰기 · 연산 · 암기", "일기 · 독서록 · 수행평가"],
             ["과제 자체가 훈련입니다.", "AI가 대신하면 훈련이", "통째로 사라집니다."]),
            ("조건부", "amber", "amberbg",
             ["조사 보고서 · 발표 준비", "내가 쓴 감상문 다듬기"],
             ["내 초안을 먼저 쓴 뒤", "점검용으로만. 쓴 사실은", "과제에 밝힙니다."]),
            ("권장", "green", "greenbg",
             ["어려운 개념 다시 설명받기", "모르는 낱말 · 아이디어 넓히기"],
             ["막힌 지점을 뚫는 용도.", "여기서 AI는 옆자리", "조교에 가깝습니다."])]
    rh = 1.16
    for i, (name, col, bg, tasks, why) in enumerate(rows):
        ry = ty + 0.44 + i * rh
        rect(s, ML + 0.06, ry, tw - 0.12, rh, fill=bg)
        if i:
            rect(s, ML + 0.06, ry, tw - 0.12, 0.012, fill="line")
        oval(s, ML + c1, ry + 0.24, 0.3, 0.3, fill=col)
        txt(s, ML + c1 + 0.42, ry + 0.22, w1, 0.35, name, size=16, bold=True, color=col)
        txt(s, ML + c2, ry + 0.24, w2, 0.7, tasks, size=12.5, color="ink", spacing=1.35)
        txt(s, ML + c3, ry + 0.2, w3, 0.85, why, size=11.5, color="body", spacing=1.3)

    bx = ML + tw + 0.35
    bw = CW - tw - 0.35
    rrect(s, bx, ty, bw, 3.92, fill="tint", line="line", radius=0.1)
    rect(s, bx + 0.3, ty + 0.35, 0.45, 0.05, fill="blue")
    txt(s, bx + 0.3, ty + 0.58, bw - 0.6, 0.8,
        ["학원 숙제는", "조금 다릅니다"], size=18, bold=True, color="ink", spacing=1.2)
    txt(s, bx + 0.3, ty + 1.5, bw - 0.6, 1.4,
        ["감당하기 어려운 ‘양’이", "원인이라면, 그건 AI를", "쓰느냐 마느냐의 문제가", "아닙니다."],
        size=13, color="body", spacing=1.4)
    rect(s, bx + 0.3, ty + 2.95, bw - 0.6, 0.012, fill="line")
    txt(s, bx + 0.3, ty + 3.12, bw - 0.6, 0.6,
        ["학원과 먼저", "상의할 문제입니다."], size=13.5, bold=True, color="blue", spacing=1.3)
    footer(s, 0, "구분 기준은 교육부·17개 시도교육청 「수행평가 시 인공지능(AI) 활용 관리 방안」의 "
                 "취지를 과제 유형에 적용한 것입니다.", link=URL_MOE_D)
    notes(s, "앞 장이 ‘지원 수준’이라는 세로축이었다면, 이 장은 ‘과제 종류’라는 가로축입니다. "
             "학부모가 집에서 바로 판단할 수 있는 형태입니다.\n"
             "빨강의 공통점을 짚어 주세요. 받아쓰기, 연산, 암기, 일기, 독서록은 결과물이 목적이 아니라 "
             "그 과정 자체가 훈련인 과제입니다. AI가 대신하면 남는 것이 없습니다.\n"
             "노랑에서 중요한 것은 순서입니다. ‘AI에게 먼저 시키고 고치기’가 아니라 ‘내가 먼저 쓰고 "
             "점검받기’입니다. 순서가 뒤집히면 노랑이 아니라 빨강이 됩니다.\n"
             "초록은 마음 놓고 권해도 되는 영역입니다. 모르는 낱말과 개념을 물어보는 것까지 막으면 "
             "아이는 부모 몰래 쓰게 됩니다.\n"
             "오른쪽 상자는 따로 시간을 들여 말씀해 주세요. ‘학원 숙제가 너무 많아 AI를 쓴다’는 상담이 "
             "실제로 자주 들어옵니다. 이건 AI 규칙으로 풀 문제가 아니라 학습량 문제이고, 학원과 상의할 "
             "일이라고 분명히 해 주시면 학부모가 안도합니다.\n"
             "주의: 표의 구분은 교육부 방안의 취지를 과제 유형에 적용해 정리한 것입니다. "
             "교육부가 과제별 목록을 이렇게 고시한 것은 아니므로, ‘참고 기준’이라고 안내해 주십시오. "
             "최종 기준은 담임 선생님의 과제 지침입니다.")
    return s


U_MIT = "https://arxiv.org/abs/2506.08872"
U_GERLICH = "https://www.mdpi.com/2075-4698/15/1/6"


def d_cogdebt(prs):
    """인지 부채와 인지적 외주화"""
    s = blank(prs)
    y = title(s, "지금 편한 만큼, 나중에 갚습니다", kicker="연구 사례",
              sub="연구자들은 이것을 ‘인지 부채(cognitive debt)’라고 부릅니다.")
    cw = (CW - 0.4) / 2
    # 왼쪽: MIT 뇌파 실험
    rrect(s, ML, y + 0.28, cw, 2.52, fill="tintblue", line=None, radius=0.1)
    txt(s, ML + 0.35, y + 0.52, cw - 0.7, 0.35, "뇌파를 재 봤더니", size=17, bold=True, color="blue")
    txt(s, ML + 0.35, y + 0.95, cw - 0.7, 0.3, "성인 54명에게 같은 글을 쓰게 한 실험",
        size=12.5, color="mute")
    bars = [("도구 없이 쓴 사람", 1.0, "blue"), ("검색으로 쓴 사람", 0.62, "teal"),
            ("AI로 쓴 사람", 0.3, "mute")]
    for i, (lab, frac, col) in enumerate(bars):
        by = y + 1.32 + i * 0.38
        txt(s, ML + 0.35, by, 2.3, 0.3, lab, size=12.5, color="ink")
        rect(s, ML + 2.75, by + 0.1, 2.5, 0.14, fill="line")
        rect(s, ML + 2.75, by + 0.1, 2.5 * frac, 0.14, fill=col)
    txt(s, ML + 0.35, y + 2.46, cw - 0.7, 0.3, "글을 쓰는 동안 뇌 영역이 이어진 정도",
        size=11, color="mute")
    # 오른쪽: 인지적 외주화
    x2 = ML + cw + 0.4
    rrect(s, x2, y + 0.28, cw, 2.52, fill="tint", line="line", radius=0.1)
    txt(s, x2 + 0.35, y + 0.52, cw - 0.7, 0.35, "‘인지적 외주화’", size=17, bold=True, color="ink")
    txt(s, x2 + 0.35, y + 0.95, cw - 0.7, 0.3, "성인 666명을 조사한 연구", size=12.5, color="mute")
    pts = ["AI를 자주 쓸수록 비판적 사고 점수가",
           "낮은 경향이 나타났습니다.",
           "생각을 밖에 맡기는 정도가 그 사이를",
           "이어 주는 고리였고, 젊은 층일수록",
           "의존이 크고 점수가 낮았습니다."]
    txt(s, x2 + 0.35, y + 1.38, cw - 0.7, 1.3, pts, size=12.5, color="body", spacing=1.35)

    rrect(s, ML, y + 2.95, CW, 0.62, fill="tint", line="line", radius=0.1)
    txt(s, ML + 0.4, y + 3.11, CW - 0.8, 0.35,
        "둘 다 성인 대상이고, 상관을 본 연구입니다. 초등학생에게 그대로 옮길 수는 없습니다.",
        size=12.5, color="mute")
    rrect(s, ML, y + 3.72, CW, 0.85, fill="ink", line=None, radius=0.1)
    txt(s, ML, y + 3.94, CW, 0.5,
        "빌린 생각은 갚아야 내 것이 됩니다. 쓰고 나서 내 말로 설명하기 — 그게 갚는 방법입니다.",
        size=16.5, bold=True, color="white", align=PP_ALIGN.CENTER)
    footer(s, 0, "출처: Kosmyna, N. et al. (2025). Your Brain on ChatGPT (MIT Media Lab) · "
                 "Gerlich, M. (2025). Societies, 15(1), 6.", link=U_MIT)
    notes(s, "{bastani}장 연구가 ‘시험 점수’를 봤다면, 이 장은 ‘머릿속에서 무슨 일이 일어나는가’를 봅니다. "
             "학부모에게 오늘 연수의 핵심 개념 하나를 남긴다면 ‘인지 부채’입니다.\n"
             "왼쪽: MIT 미디어랩 연구진이 성인 54명에게 에세이를 쓰게 하면서 뇌파(EEG)를 측정했습니다. "
             "도구 없이 쓴 그룹의 뇌 연결이 가장 넓고 강했고, 검색엔진 그룹이 중간, AI 그룹이 가장 약했습니다. "
             "AI로 쓴 사람들은 조금 전 자기가 쓴 글을 인용하지 못했고, ‘내 글’이라는 느낌도 약했습니다. "
             "연구진은 이를 ‘인지 부채’라고 불렀습니다. 당장은 편하지만 나중에 갚아야 하는 빚이라는 뜻입니다.\n"
             "오른쪽: 성인 666명을 조사한 다른 연구에서는 AI를 자주 쓸수록 비판적 사고 점수가 낮은 경향이 "
             "나타났고, ‘인지적 외주화’(생각을 밖에 맡기는 것)가 그 사이를 매개했습니다. "
             "젊은 층일수록 의존이 크고 점수가 낮았습니다.\n"
             "해석의 한계를 반드시 함께 말해 주십시오. ①둘 다 성인 대상입니다. ②MIT 연구는 54명의 "
             "소규모 실험이고 아직 학계 논의가 진행 중입니다(반론 논문도 나와 있습니다). "
             "③두 번째 연구는 상관 분석이라 ‘AI 때문에 사고력이 낮아졌다’고 단정할 수 없습니다. "
             "‘생각을 많이 맡기는 사람이 원래 그렇다’는 반대 설명도 가능합니다.\n"
             "가정에서의 실천은 이미 배운 것과 같습니다. 화면을 닫고 자기 말로 설명하게 하기. "
             "그것이 빌린 생각을 갚는 절차라고 정리해 주세요.")
    return s


def d_together(prs):
    """빌려주는 게 아니라 함께 쓰기 — 동반 사용과 단독 사용"""
    s = blank(prs)
    y = title(s, "빌려주는 게 아니라, 함께 씁니다", kicker="사용 방식",
              sub="부모 계정을 쓴다면 방식도 정해 둬야 합니다. 두 단계로 나눠 보세요.")
    cw = (CW - 0.4) / 2
    card(s, ML, y + 0.3, cw, 2.15, "보호자와 함께 쓰기",
         ["· 무엇을 알아볼지 먼저 정합니다",
          "· 어떤 정보를 넣을지 함께 봅니다",
          "· 언제 끝낼지 미리 약속합니다"],
         fill="tintblue", line=None, accent="blue", head_size=18, body_size=13.5)
    card(s, ML + cw + 0.4, y + 0.3, cw, 2.15, "아이 혼자 쓰기",
         ["· 준비도 네 가지를 갖췄을 때({ready}장)",
          "· 사용 목적과 시간을 정해 둔 상태에서",
          "· 무엇을 물었는지 나중에 이야기하기로"],
         fill="tint", line="line", accent="teal", head_size=18, body_size=13.5)
    rrect(s, ML, y + 2.65, CW, 1.0, fill="tint", line="line", radius=0.1)
    txt(s, ML + 0.4, y + 2.85, CW - 0.8, 0.62,
        ["‘함께 쓰기’는 옆에 앉아 지켜보라는 뜻이 아닙니다. 시작 전에 세 가지를 정하고,",
         "끝난 뒤 무엇을 알게 됐는지 한 번 물어보는 것으로 충분합니다."],
        size=13.5, color="body", spacing=1.4)
    rrect(s, ML, y + 3.8, CW, 0.82, fill="tintteal", line=None, radius=0.1)
    txt(s, ML + 0.4, y + 4.0, CW - 0.8, 0.45,
        "혼자 쓰기로 넘어가는 시점은 나이가 아니라, 위 세 가지를 스스로 지킬 수 있을 때입니다.",
        size=15, bold=True, color="teal")
    footer(s, 0)
    notes(s, "계정은 부모 것이라도 실제로 쓰는 사람은 아이입니다. 그래서 방식을 정해 둬야 합니다.\n"
             "왼쪽 세 가지가 이 연수에서 가장 실천하기 쉬운 부분입니다. "
             "①무엇을 알아볼지 ②어떤 정보를 넣을지 ③언제 끝낼지. "
             "이 세 문장은 {familylink}장 Family Link 설정에서도, {promise}장 우리 집 약속에서도 그대로 나옵니다.\n"
             "오른쪽은 조건입니다. {ready}장의 준비도 네 가지를 갖추고, 목적과 시간을 정해 두고, "
             "나중에 무엇을 물었는지 이야기하기로 한 상태여야 합니다. "
             "셋 중 하나라도 빠지면 아직 왼쪽 단계입니다.\n"
             "학부모가 자주 하는 오해를 풀어 주세요. ‘함께 쓴다’는 것이 내내 옆에 붙어 있으라는 뜻이 "
             "아닙니다. 시작 전 3분, 끝난 뒤 1분이면 충분합니다.\n"
             "넘어가는 시점을 묻는 질문에는 나이로 답하지 마시고, 아래 띠의 기준으로 답해 주십시오.")
    return s


def d_five(prs):
    """AI가 바뀌어도 남는 다섯 가지"""
    s = blank(prs)
    y = title(s, "제품이 바뀌어도 남는 다섯 가지", kicker="준비시킬 것",
              sub="특정 AI의 조작법보다, 어디서나 쓰이는 다섯 가지가 먼저입니다.")
    items = [("문서로 정리하기", "생각을 글과 표로\n옮기는 힘"),
             ("검색어 만들기", "무엇을 찾을지\n말로 좁히는 힘"),
             ("표·그래프 읽기", "숫자가 무엇을 말하는지\n읽어 내는 힘"),
             ("출처 표시하기", "누구의 말인지\n밝히는 습관"),
             ("개인정보 관리하기", "무엇을 남기지 않을지\n판단하는 힘")]
    cw = (CW - 4 * 0.26) / 5
    for i, (h, b) in enumerate(items):
        x = ML + i * (cw + 0.26)
        rrect(s, x, y + 0.3, cw, 2.35, fill="tint", line="line", radius=0.1)
        numbadge(s, x + cw / 2 - 0.21, y + 0.55, 0.42, i + 1, fill="teal")
        txt(s, x + 0.12, y + 1.18, cw - 0.24, 0.5, h, size=14.5, bold=True, color="ink",
            align=PP_ALIGN.CENTER, spacing=1.2)
        txt(s, x + 0.12, y + 1.8, cw - 0.24, 0.6, b.split("\n"), size=12, color="body",
            align=PP_ALIGN.CENTER, spacing=1.3)
    rrect(s, ML, y + 2.95, CW, 1.15, fill="tintteal", line=None, radius=0.1)
    rich(s, ML + 0.4, y + 3.16, CW - 0.8, 0.72,
         [[("AI 제품은 몇 년 뒤면 또 바뀝니다. ", "body", False),
           ("위의 다섯 가지는 그대로 남습니다.", "teal", True)],
          [("AI는 이걸 하다가 막힐 때 도움을 얻는 방법으로 익히면 충분합니다.", "body", False)]],
         size=14.5, spacing=1.35, space_after=4)
    footer(s, 0)
    notes(s, "앞 장이 ‘언제 무엇부터’였다면, 이 장은 ‘AI가 바뀌어도 남는 것’입니다. "
             "{tower}장의 3층 구조와 짝으로 보시면 됩니다.\n"
             "‘우리 아이만 뒤처지는 것 아닌가’라는 불안에 답하는 장입니다. "
             "특정 제품 사용법을 일찍 배우는 것이 경쟁력이 되지 않는다는 점을 분명히 하되, "
             "‘그러니 안 해도 된다’로 들리지 않게 균형을 잡아 주십시오. "
             "다섯 가지는 AI가 없어도 필요한 능력이고, AI가 있으면 더 잘 쓰이는 능력입니다.\n"
             "두 번째 ‘검색어 만들기’는 {formula}장 프롬프트 공식과 같은 능력입니다. "
             "내가 무엇을 모르는지 한 문장으로 말하는 힘이라고 이어 주세요.\n"
             "네 번째와 다섯 번째는 앞 장에서 ‘모든 층에 걸친다’고 말한 바로 그 두 가지입니다.\n"
             "시간이 부족하면 앞 장(3층)만 하고 이 장은 유인물로 대체하셔도 됩니다.")
    return s
