# -*- coding: utf-8 -*-
"""슬라이드 1~10"""
from deckkit import *
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

SRC_KPF = "출처: 한국언론진흥재단, 『2025 10대 청소년 미디어 이용 조사』(초4~고3 2,674명)"
URL_KPF = "https://www.kpf.or.kr/front/research/consumerDetail.do?seq=600223"
URL_PNAS = "https://www.pnas.org/doi/10.1073/pnas.2422633122"
URL_MOE = ("https://www.moe.go.kr/boardCnts/viewRenew.do?boardID=294&boardSeq=104984"
           "&lev=0&m=020402")
URL_NYPI = "https://www.nypi.re.kr/repository/handle/2022.oak/6296"
SRC_PNAS = ("출처: Bastani, H. et al. (2025). Generative AI without guardrails can harm learning: "
            "Evidence from high school mathematics. PNAS 122(26).")
SRC_MOE = "출처: 교육부·17개 시도교육청, 「수행평가 시 인공지능(AI) 활용 관리 방안」"
SRC_NYPI = ("출처: 한국청소년정책연구원, 『청소년의 생성형 AI 이용실태 및 리터러시 증진방안 연구』"
            "(연구보고 24-기본02) · 중·고등학생 대상 조사")


def s01(prs):
    s = blank(prs)
    rect(s, 0, 0, W, 0.16, fill="blue")
    txt(s, ML, 1.55, 6.4, 0.3, "학부모 연수", size=14, bold=True, color="teal")
    rect(s, ML, 1.92, 0.72, 0.06, fill="blue")
    txt(s, ML, 2.25, 6.6, 1.9,
        ["AI 시대,", "우리 아이의 미래를 준비하는 부모 교육"],
        size=36, bold=True, color="ink", spacing=1.18)
    txt(s, ML, 4.32, 6.5, 0.8,
        ["학교의 AI 교육부터", "가정에서 실천하는 올바른 AI 활용법까지"],
        size=16, color="mute", spacing=1.35)
    rrect(s, ML, 5.55, 4.25, 0.56, fill="tintblue", line=None, radius=0.3)
    txt(s, ML, 5.71, 4.25, 0.3, "2026. 9. 17.(목)  15:00 ~ 16:30",
        size=14.5, bold=True, color="blue", align=PP_ALIGN.CENTER)

    # 오늘 연수가 바꾸려는 한 장면
    bx, by, bw = 7.75, 2.05, 4.7
    rrect(s, bx, by, bw, 1.2, fill="tint", line="line", radius=0.12)
    txt(s, bx + 0.34, by + 0.26, 1.0, 0.3, "아이", size=12, bold=True, color="teal")
    txt(s, bx + 0.34, by + 0.6, bw - 0.7, 0.4, "“이거 AI한테 물어봐도 돼요?”",
        size=16, color="ink")
    arrow(s, bx + bw / 2 - 0.17, by + 1.34, 0.34, 0.38, fill="line")
    sh = s.shapes[-1]
    sh.rotation = 90
    rrect(s, bx, by + 1.95, bw, 1.2, fill="tintblue", line=None, radius=0.12)
    txt(s, bx + 0.34, by + 2.21, 1.2, 0.3, "부모", size=12, bold=True, color="blue")
    txt(s, bx + 0.34, by + 2.55, bw - 0.7, 0.4, "“먼저 네 생각은 어때?”",
        size=16, bold=True, color="ink")
    txt(s, bx, by + 3.4, bw, 0.34, "오늘 바꿔 보려는 건 이 한 장면입니다.",
        size=12.5, color="mute", align=PP_ALIGN.CENTER)
    notes(s, "인사와 함께 오늘의 결론을 먼저 보여 줍니다. "
             "‘AI를 쓰게 할까 말까’가 아니라 ‘아이의 생각을 지키면서 어떻게 쓰게 할까’가 오늘의 질문임을 밝힙니다. "
             "90분 동안 설명만 듣는 시간이 아니라 여섯 번의 짧은 참여 활동이 있다고 예고합니다.")
    return s


def s02(prs):
    s = blank(prs)
    y = title(s, "우리 집에서는 어떤 일이 생기나요?",
              kicker="여는 활동 · 손들기", sub="가장 가까운 것 하나에 손을 들어 주세요.")
    items = [
        ("숙제를 맡겨요", "물어보면 답이 바로 나오니\n먼저 AI부터 켭니다."),
        ("계속 물어봐요", "생각하기 전에\n습관처럼 AI를 찾습니다."),
        ("답을 믿어요", "틀린 내용도\n그대로 받아 적습니다."),
        ("시작이 걱정돼요", "언제부터 어디까지\n허용할지 모르겠습니다."),
    ]
    cw, gap = 2.68, 0.31
    for i, (h, b) in enumerate(items):
        x = ML + i * (cw + gap)
        card(s, x, y + 0.12, cw, 2.5, h, b.split("\n"),
             fill="tint", line="line", accent="blue", head_size=18, body_size=13.5)
    rrect(s, ML, y + 2.95, CW, 1.0, fill="tintteal", line=None, radius=0.1)
    rich(s, ML + 0.4, y + 3.18, CW - 0.8, 0.6,
         [[("우리 집만의 고민이 아닙니다. ", "body", False),
           ("초등 4~6학년 51.2%", "teal", True),
           ("가 최근 일주일 안에 AI를 이용했습니다. 중학생 69.8%, 고등학생 82.3%.", "body", False)]],
         size=16)
    footer(s, 2, SRC_KPF, link=URL_KPF)
    notes(s, "네 가지를 읽어 주고 손을 들게 합니다. 가장 많이 나온 항목을 기억해 두었다가 "
             "해당 구간(숙제=22~27장, 사실 확인=30~31장, 시작 나이=10~16장)에서 다시 언급하면 몰입도가 올라갑니다.\n"
             "수치 안내: 한국언론진흥재단 『2025 10대 청소년 미디어 이용 조사』, 초4~고3 2,674명 대상, "
             "‘최근 일주일 내 인공지능 이용’ 응답 기준(전체 67.6%). 매일 이용은 초등 3.7%로 아직 낮습니다. "
             "‘많이 쓴다’가 아니라 ‘이미 접하고 있다’는 뜻으로 해석해 주십시오.")
    return s


def s03(prs):
    s = blank(prs)
    y = title(s, "오늘 가져갈 세 가지", kicker="연수의 목표",
              sub="오늘은 이 세 가지만 들고 가셔도 충분합니다.")
    items = [("사용 기준", "몇 살부터,\n어디까지 허용할까", "blue", "tintblue"),
             ("숙제 원칙", "무엇이 도움이고\n무엇이 대행일까", "teal", "tintteal"),
             ("확인 습관", "이 답이 정말\n맞는지 어떻게 볼까", "blue", "tintblue")]
    d = 2.45
    total = 3 * d + 2 * 0.85
    x0 = (W - total) / 2
    for i, (h, b, col, bg) in enumerate(items):
        x = x0 + i * (d + 0.85)
        oval(s, x, y + 0.35, d, d, fill=bg)
        txt(s, x, y + 1.18, d, 0.4, h, size=21, bold=True, color=col, align=PP_ALIGN.CENTER)
        txt(s, x - 0.1, y + 3.0, d + 0.2, 0.9, b.split("\n"), size=14, color="body",
            align=PP_ALIGN.CENTER, spacing=1.3)
        if i < 2:
            txt(s, x + d + 0.12, y + 1.3, 0.6, 0.4, "+", size=24, bold=True,
                color="line", align=PP_ALIGN.CENTER)
    footer(s, 3)
    notes(s, "세 가지를 손가락으로 세어 보이며 말합니다. "
             "‘AI를 얼마나 일찍 배우느냐’보다 ‘아이의 생각을 지키면서 어떻게 쓰느냐’가 오늘의 축이라고 분명히 합니다.")
    return s


def s04(prs):
    s = blank(prs)
    y = title(s, "AI가 맞히면, 아이도 배운 것이다?",
              kicker="OX 퀴즈 · 먼저 투표", sub="답을 보기 전에 O 또는 X로 손을 들어 주세요.")
    bw = 2.1
    oval(s, ML + 1.15, y + 0.2, bw, bw, fill="tint")
    txt(s, ML + 1.15, y + 0.95, bw, 0.6, "O", size=44, bold=True, color="mute", align=PP_ALIGN.CENTER)
    oval(s, ML + 1.15 + bw + 0.6, y + 0.2, bw, bw, fill="tintblue")
    txt(s, ML + 1.15 + bw + 0.6, y + 0.95, bw, 0.6, "X", size=44, bold=True, color="blue", align=PP_ALIGN.CENTER)
    txt(s, ML + 1.15 + bw + 0.6, y + 2.45, bw, 0.34, "정답", size=13, bold=True,
        color="blue", align=PP_ALIGN.CENTER)

    x = 7.05
    txt(s, x, y + 0.25, CW - (x - ML), 0.8,
        "문제를 푼 건 AI입니다.\n아이는 그걸 지켜봤을 뿐입니다.", size=19, bold=True,
        color="ink", spacing=1.3)
    cw = (CW - (x - ML) - 0.3) / 2
    card(s, x, y + 1.15, cw, 1.95, "답을 얻기",
         ["· 과제가 끝난다", "· 오늘 점수는 오른다", "· 다음에 또 막힌다"],
         fill="tint", line="line", head_size=16, body_size=13.5)
    card(s, x + cw + 0.3, y + 1.15, cw, 1.95, "스스로 설명하기",
         ["· 시간이 걸린다", "· 오늘은 더디다", "· 다음에 혼자 푼다"],
         fill="tintblue", line=None, accent="blue", head_size=16, body_size=13.5)
    rrect(s, x, y + 3.25, CW - (x - ML), 0.92, fill="tintteal", line=None, radius=0.12)
    txt(s, x + 0.3, y + 3.47, CW - (x - ML) - 0.6, 0.6,
        "확인은 간단합니다. 화면을 닫고 아이에게 설명해 보라고 해 보세요.",
        size=14, bold=True, color="teal", spacing=1.3)
    footer(s, 4)
    notes(s, "정답은 X입니다. 투표 결과를 먼저 세어 보고 시작하면 다음 장의 연구 결과가 훨씬 잘 들립니다.\n"
             "여기서 결론을 길게 설명하지 마십시오. 5~9장에서 근거를 제시합니다. "
             "‘화면을 닫고 설명하게 하기’는 오늘 연수에서 반복되는 핵심 장치입니다.")
    return s


def s05(prs):
    s = blank(prs)
    y = title(s, "AI는 어떻게 그럴듯한 답을 만들까요?",
              kicker="원리 이해", sub="복잡한 기술은 아닙니다. 알아 두면 어디를 확인해야 할지 감이 옵니다.")
    steps = [("질문을 입력합니다", "아이가 쓴 문장이\n그대로 들어갑니다"),
             ("이어질 말을 예측합니다", "학습한 방대한 글에서\n가장 그럴듯한 말을 고릅니다"),
             ("문장으로 만들어 냅니다", "사실 여부를 확인한 것이\n아니라 문장을 완성한 것입니다")]
    cw, gap = 3.5, 0.55
    x0 = ML
    for i, (h, b) in enumerate(steps):
        x = x0 + i * (cw + gap)
        rrect(s, x, y + 0.25, cw, 1.95, fill="tint" if i < 2 else "tintblue",
              line="line" if i < 2 else None, radius=0.1)
        numbadge(s, x + 0.3, y + 0.52, 0.42, i + 1, fill="blue" if i == 2 else "teal")
        txt(s, x + 0.3, y + 1.12, cw - 0.6, 0.4, h, size=16.5, bold=True, color="ink")
        txt(s, x + 0.3, y + 1.52, cw - 0.6, 0.6, b.split("\n"), size=13, color="body", spacing=1.3)
        if i < 2:
            arrow(s, x + cw + 0.1, y + 1.05, 0.35, 0.3, fill="line")
    rrect(s, ML, y + 2.62, CW, 1.38, fill="tintteal", line=None, radius=0.1)
    rich(s, ML + 0.4, y + 2.84, CW - 0.8, 1.0,
         [[("그래서 AI는 ", "body", False), ("모르면 ‘모른다’고 하기보다 그럴듯하게 채웁니다.", "teal", True)],
          [("검색으로 최신 자료까지 찾아 주는지, 계산은 따로 도구를 쓰는지는 서비스마다 다릅니다. "
            "우리 아이가 쓰는 게 어느 쪽인지부터 보시면 좋겠습니다.", "body", False)]],
         size=14.5, spacing=1.35, space_after=5)
    footer(s, 5)
    notes(s, "비유: ‘엄청나게 많은 글을 읽고 다음에 올 말을 아주 잘 맞히는 프로그램’. "
             "‘정답을 찾아 주는 기계’가 아니라 ‘문장을 완성하는 기계’라는 점이 핵심입니다.\n"
             "여기서 ‘환각(hallucination)’이라는 용어를 한 번만 언급하고 넘어가되, 30장에서 다시 다룬다고 예고합니다. "
             "서비스마다 검색 연결 여부가 다르므로 특정 제품의 특성을 모든 AI로 일반화하지 않도록 주의합니다.")
    return s


def s06(prs):
    s = blank(prs)
    y = title(s, "같은 정답, 다른 공부", kicker="갈림길",
              sub="모르는 문제를 만난 순간, 두 갈래로 나뉩니다.")
    rrect(s, ML, y + 1.45, 2.35, 0.95, fill="tint", line="line", radius=0.12)
    txt(s, ML + 0.25, y + 1.72, 1.9, 0.5, ["모르는 문제를", "만났다"], size=15.5,
        bold=True, color="ink", spacing=1.25)
    arrow(s, ML + 2.5, y + 1.78, 0.42, 0.3, fill="line")

    x = ML + 3.1
    cw = CW - 3.1
    rrect(s, x, y + 0.3, cw, 1.4, fill="tint", line="line", radius=0.1)
    txt(s, x + 0.3, y + 0.52, 2.2, 0.35, "A. 답을 복사한다", size=15.5, bold=True, color="mute")
    txt(s, x + 0.3, y + 0.95, cw - 0.6, 0.45,
        "과제는 끝난다  →  오늘 점수는 오른다  →  다음에 또 막힌다",
        size=14.5, color="body")
    rrect(s, x, y + 2.05, cw, 1.4, fill="tintblue", line=None, radius=0.1)
    txt(s, x + 0.3, y + 2.27, 3.0, 0.35, "B. 힌트를 받아 다시 푼다", size=15.5, bold=True, color="blue")
    txt(s, x + 0.3, y + 2.7, cw - 0.6, 0.45,
        "시간이 걸린다  →  오늘은 더디다  →  다음에 혼자 푼다",
        size=14.5, color="body")
    rrect(s, ML, y + 3.75, CW, 0.78, fill="tintteal", line=None, radius=0.12)
    txt(s, ML + 0.4, y + 3.97, CW - 0.8, 0.4,
        "같은 AI, 같은 문제입니다. 아이가 무엇을 요청했느냐만 달랐습니다.",
        size=16, bold=True, color="teal")
    footer(s, 6)
    notes(s, "A와 B는 같은 AI, 같은 문제입니다. 다른 것은 아이가 무엇을 요청했는가뿐입니다. "
             "26장 ‘답 알려줘를 바꿔봅시다’ 활동이 바로 이 갈림길을 B로 돌리는 연습이라고 연결해 주십시오.")
    return s


def s07(prs):
    s = blank(prs)
    y = title(s, "연구를 볼 때 꼭 물어볼 세 가지", kicker="자료 읽는 법",
              sub="기사 제목만 보고 판단하지 않기 위한 최소한의 질문입니다.")
    qs = [("누구를 대상으로 했나?", "초등학생인지 고등학생인지,\n어느 나라 학생인지에 따라\n결과는 달라집니다."),
          ("무엇을 측정했나?", "과제 점수인지, 시험 점수인지,\n아니면 흥미나 만족도인지\n구분해야 합니다."),
          ("AI 없이도 잘했나?", "AI를 쓰는 동안의 점수와\nAI를 치운 뒤의 실력은\n같지 않습니다.")]
    cw, gap = 3.6, 0.42
    for i, (h, b) in enumerate(qs):
        x = ML + i * (cw + gap)
        rrect(s, x, y + 0.3, cw, 2.75, fill="tint", line="line", radius=0.1)
        numbadge(s, x + 0.32, y + 0.58, 0.44, i + 1, fill="teal")
        txt(s, x + 0.32, y + 1.22, cw - 0.64, 0.45, h, size=17.5, bold=True, color="ink", spacing=1.15)
        txt(s, x + 0.32, y + 1.78, cw - 0.64, 1.0, b.split("\n"), size=13.5, color="body", spacing=1.35)
    rrect(s, ML, y + 3.4, CW, 0.82, fill="tintblue", line=None, radius=0.12)
    txt(s, ML + 0.4, y + 3.63, CW - 0.8, 0.4,
        "다음 장에서 볼 연구도 이 순서대로 한번 따져 보겠습니다.",
        size=15.5, bold=True, color="blue")
    footer(s, 7)
    notes(s, "학부모가 기사에서 만나는 ‘AI가 성적을 올린다 / 떨어뜨린다’ 류의 상반된 제목을 스스로 판단하도록 돕는 장입니다.\n"
             "세 번째 질문이 오늘 연수에서 가장 중요합니다. 대부분의 낙관적 보도는 ‘AI를 쓰는 동안’의 성과를 다룹니다.")
    return s


def s08(prs):
    s = blank(prs)
    y = title(s, "AI를 쓰는 동안과, 끈 다음은 다릅니다", kicker="연구 사례",
              sub="튀르키예의 한 고등학교에서 약 1,000명을 대상으로 한 수학 실험입니다.")
    cw = (CW - 0.4) / 2
    # 왼쪽: AI를 쓰는 동안
    rrect(s, ML, y + 0.25, cw, 3.05, fill="tintblue", line=None, radius=0.1)
    txt(s, ML + 0.35, y + 0.52, cw - 0.7, 0.35, "연습 문제를 푸는 동안 (AI 있음)",
        size=15, bold=True, color="blue")
    rows = [("일반 챗봇을 쓴 학생", "+48%"), ("학습용 튜터를 쓴 학생", "+127%")]
    for i, (lab, val) in enumerate(rows):
        yy = y + 1.05 + i * 0.95
        txt(s, ML + 0.35, yy + 0.16, cw - 2.4, 0.4, lab, size=14.5, color="body")
        txt(s, ML + cw - 2.35, yy, 2.0, 0.55, val, size=30, bold=True, color="blue",
            align=PP_ALIGN.RIGHT)
    txt(s, ML + 0.35, y + 2.85, cw - 0.7, 0.3,
        "AI를 쓰지 않은 학생 대비 정답률", size=12, color="mute")
    # 오른쪽: AI를 치운 뒤
    x2 = ML + cw + 0.4
    rrect(s, x2, y + 0.25, cw, 3.05, fill="tint", line="line", radius=0.1)
    txt(s, x2 + 0.35, y + 0.52, cw - 0.7, 0.35, "AI 없이 본 시험 (AI 치운 뒤)",
        size=15, bold=True, color="ink")
    txt(s, x2 + 0.35, y + 1.21, cw - 2.4, 0.4, "일반 챗봇을 쓴 학생", size=14.5, color="body")
    txt(s, x2 + cw - 2.35, y + 1.05, 2.0, 0.55, "−17%", size=30, bold=True,
        color="red", align=PP_ALIGN.RIGHT)
    txt(s, x2 + 0.35, y + 2.16, cw - 2.4, 0.4, "학습용 튜터를 쓴 학생", size=14.5, color="body")
    txt(s, x2 + cw - 2.6, y + 2.02, 2.25, 0.5, "차이 거의 없음", size=17, bold=True,
        color="teal", align=PP_ALIGN.RIGHT)
    txt(s, x2 + 0.35, y + 2.85, cw - 0.7, 0.3,
        "AI를 아예 쓰지 않은 학생과 비교한 결과", size=12, color="mute")

    rrect(s, ML, y + 3.45, CW, 1.15, fill="tintteal", line=None, radius=0.12)
    rich(s, ML + 0.4, y + 3.64, CW - 0.8, 0.8,
         [[("차이를 만든 것은 설정이었습니다. ", "body", False),
           ("정답을 바로 주지 않고 교사가 설계한 힌트를 주도록 했더니 부정적 효과가 대부분 사라졌습니다.",
            "teal", True)],
          [("고등학생 대상 수학 실험이므로 초등학생에게 그대로 적용할 수는 없습니다.", "body", False)]],
         size=14.5, spacing=1.35, space_after=4)
    footer(s, 8, SRC_PNAS, link=URL_PNAS)
    notes(s, "이 장은 오늘 연수의 근거 중심입니다. 천천히 읽어 주십시오.\n"
             "연구 개요: 튀르키예의 한 고등학교, 2023–24학년도 1학기, 고등학생 약 1,000명, 수학 연습 문제. "
             "두 가지 AI를 비교했습니다. ①일반 챗봇과 같은 인터페이스(GPT Base) ②정답 대신 교사가 설계한 힌트를 주도록 "
             "안전장치를 넣은 튜터(GPT Tutor).\n"
             "결과: 연습 중에는 각각 48%, 127% 성적이 올랐지만, AI를 치우고 본 시험에서 일반 챗봇을 쓴 학생은 "
             "AI를 쓴 적 없는 학생보다 17% 낮았습니다. 튜터 쪽은 부정적 효과가 대부분 사라졌습니다.\n"
             "해석의 한계를 반드시 함께 말해 주십시오. ①고등학생 대상이므로 초등학생에게 그대로 적용할 수 없습니다. "
             "②수학 연습 문제라는 특정 과제입니다. ③‘AI가 나쁘다’가 아니라 ‘안전장치 없이 정답을 주는 방식이 위험하다’는 연구입니다. "
             "논문 제목 자체가 ‘without guardrails(안전장치 없이)’입니다.\n"
             "인용 시 참고: 해당 논문에는 2025년 8월 정정 공지(Correction)가 함께 게재되어 있으므로, "
             "자료집에 옮길 때 PNAS 최종본을 확인하시기 바랍니다.")
    return s


def s09(prs):
    s = blank(prs)
    y = title(s, "그렇다면 몇 살부터 시작할까요?", kicker="시작 나이",
              sub="모든 AI에 통하는 하나의 나이는 없습니다. 세 관문을 차례로 확인합니다.")
    gates = [("서비스 이용 조건", "쓰려는 서비스의 약관이\n정한 나이와 동의 요건",
              "가장 먼저 확인"),
             ("학교 지침", "학교가 안내한 사용 범위와\n과제에서의 허용 여부", "두 번째"),
             ("아이의 준비도", "나이와 별개로\n아이가 갖췄는지 볼 것", "마지막")]
    cw, gap = 3.55, 0.48
    for i, (h, b, tag) in enumerate(gates):
        x = ML + i * (cw + gap)
        rrect(s, x, y + 0.3, cw, 2.5, fill="tintblue" if i == 0 else "tint",
              line=None if i == 0 else "line", radius=0.1)
        txt(s, x + 0.32, y + 0.55, cw - 0.64, 0.28, tag, size=11.5, bold=True,
            color="blue" if i == 0 else "mute")
        txt(s, x + 0.32, y + 0.95, cw - 0.64, 0.4, h, size=18, bold=True, color="ink")
        txt(s, x + 0.32, y + 1.5, cw - 0.64, 0.8, b.split("\n"), size=13.5,
            color="body", spacing=1.35)
        if i < 2:
            txt(s, x + cw + 0.05, y + 1.3, 0.4, 0.4, "›", size=26, bold=True,
                color="line", align=PP_ALIGN.CENTER)
    rrect(s, ML, y + 3.15, CW, 0.8, fill="tintteal", line=None, radius=0.12)
    rich(s, ML + 0.4, y + 3.36, CW - 0.8, 0.45,
         [[("나이가 됐다고 바로 혼자 써도 된다는 뜻은 아닙니다. ", "teal", True),
           ("세 가지를 다 확인하셨다면, 그때 시작하셔도 좋습니다.", "body", False)]],
         size=15)
    footer(s, 9)
    notes(s, "학부모가 가장 많이 묻는 질문이지만, 하나의 숫자로 답하지 않는 것이 정확합니다.\n"
             "다음 장에서 세 번째 관문(준비도)을, 14장에서 첫 번째 관문(서비스별 연령 조건)을 구체적으로 다룹니다. "
             "두 번째 관문(학교 지침)은 12~13장, 22장입니다.")
    return s


def s10(prs):
    s = blank(prs)
    y = title(s, "나이와 별도로 확인할 준비도", kicker="세 번째 관문",
              sub="네 가지가 되면 혼자 쓰는 연습을 시작할 수 있습니다.")
    items = [("틀릴 수 있음을 이해하기",
              "“AI도 틀려요”라고 말할 수 있고,\n실제로 틀린 답을 본 경험이 있습니다."),
             ("개인정보를 구분하기",
              "이름·학교·주소·사진은\n입력하지 않아야 한다는 것을 압니다."),
             ("자기 말로 설명하기",
              "받은 답을 그대로 읽지 않고\n자기 문장으로 바꿔 말할 수 있습니다."),
             ("스스로 멈추기",
              "약속한 시점에 화면을 닫고\n다른 활동으로 넘어갈 수 있습니다.")]
    cw, gap = (CW - 0.4) / 2, 0.4
    for i, (h, b) in enumerate(items):
        x = ML + (i % 2) * (cw + gap)
        yy = y + 0.3 + (i // 2) * 1.62
        rrect(s, x, yy, cw, 1.42, fill="tint", line="line", radius=0.1)
        numbadge(s, x + 0.34, yy + 0.32, 0.42, i + 1, fill="teal")
        txt(s, x + 1.0, yy + 0.3, cw - 1.35, 0.4, h, size=17, bold=True, color="ink")
        txt(s, x + 1.0, yy + 0.72, cw - 1.35, 0.6, b.split("\n"), size=13, color="body", spacing=1.3)
    rrect(s, ML, y + 3.72, CW, 0.78, fill="tintblue", line=None, radius=0.12)
    txt(s, ML + 0.4, y + 3.93, CW - 0.8, 0.4,
        "아직 이르다 싶으면 막지 마시고, 옆에서 같이 쓰는 단계로 두세요.",
        size=15.5, bold=True, color="blue")
    footer(s, 10)
    notes(s, "이 네 가지는 집에서 5분이면 확인할 수 있습니다. 실제로 틀린 답을 하나 같이 찾아보는 것이 "
             "가장 빠른 방법입니다(31장 활동과 연결).\n"
             "‘아직 안 됨 = 금지’가 아니라 ‘아직 안 됨 = 동반 사용’이라는 메시지를 꼭 전해 주십시오. "
             "금지만 하면 아이는 부모가 모르는 곳에서 씁니다.")
    return s
