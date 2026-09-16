# -*- coding: utf-8 -*-
"""슬라이드 21~30"""
from deckkit import *
from slides_a import SRC_KPF, SRC_PNAS, SRC_MOE, SRC_NYPI, URL_KPF, URL_MOE, URL_NYPI
from slides_b import URL_OPENAI_PC
from pptx.enum.text import PP_ALIGN


def s21(prs):
    s = blank(prs)
    y = title(s, "AI 프롬프트 공식, 네 칸만 채우면 됩니다", kicker="프롬프트 공식",
              sub="외울 것은 네 가지뿐입니다. 아이가 이 형식만 익히면 돌아오는 답이 달라집니다.")
    items = [("내 수준", "“초등학교 4학년이야”"), ("내 시도", "“분모끼리 더했어”"),
             ("필요한 도움", "“어디가 틀렸는지 궁금해”"), ("답변 방식", "“정답 말고 질문으로 해 줘”")]
    gap = 0.38
    cw = (CW - 3 * gap) / 4
    for i, (h, ex) in enumerate(items):
        x = ML + i * (cw + gap)
        rrect(s, x, y + 0.28, cw, 1.88, fill="tintblue", line=None, radius=0.1)
        numbadge(s, x + 0.26, y + 0.5, 0.38, i + 1, fill="blue", size=13)
        txt(s, x + 0.26, y + 1.0, cw - 0.52, 0.32, h, size=16, bold=True, color="ink")
        txt(s, x + 0.26, y + 1.34, cw - 0.52, 0.7, ex, size=12, color="blue", spacing=1.25)
        if i < 3:
            txt(s, x + cw, y + 1.04, gap, 0.36, "+", size=20, bold=True,
                color="mute", align=PP_ALIGN.CENTER)
    rrect(s, ML, y + 2.36, CW, 2.2, fill="tint", line="line", radius=0.1)
    rich(s, ML + 0.4, y + 2.56, 7.0, 0.3,
         [[("=  ", "blue", True), ("네 칸을 이어 붙이면 이런 한 문장이 됩니다", "teal", True)]],
         size=13)
    rect(s, ML + 0.4, y + 2.94, 0.05, 1.4, fill="blue")
    txt(s, ML + 0.7, y + 2.94, CW - 1.3, 1.45,
        ["나는 초등학교 4학년이야. 분모가 다른 분수의 덧셈을 공부하고 있어.",
         "분모끼리 더했는데 왜 틀렸는지 모르겠어.",
         "정답을 바로 말하지 말고, 그림으로 생각할 수 있는 질문을 하나씩 해 줘."],
        size=16, color="ink", spacing=1.45, space_after=3)
    footer(s, 23)
    notes(s, "이 프롬프트는 유인물에 그대로 넣어 드리는 것이 좋습니다. 부모가 아이 옆에서 한 번만 같이 써 보면 "
             "아이가 형식을 금방 익힙니다.\n"
             "네 번째(답변 방식)가 핵심입니다. 8장 연구에서 효과를 만든 것이 바로 이 부분, "
             "즉 ‘정답 대신 힌트’ 설정이었습니다.\n"
             "주의: 좋은 공식이 답을 유용하게 만들어 주지만 정확성까지 보장하지는 않습니다. 30장에서 이어집니다.")
    return s


def s22(prs):
    s = blank(prs)
    y = title(s, "틈만 나면 AI를 찾는 아이에게", kicker="사용 습관",
              sub="막기보다, 쓰기 전과 쓴 뒤에 한마디씩 붙여 보세요.")
    steps = [("쓰기 전", "“먼저 네 생각은?”", "이미 아는 것 하나,\n궁금한 것 하나를 말하게 합니다."),
             ("쓰는 중", "“무엇을 도와달라고 할까?”", "설명인지 힌트인지 피드백인지\n먼저 정하게 합니다."),
             ("쓴 뒤", "“화면 닫고 설명해 볼까?”", "자기 말로 옮기지 못하면\n아직 배운 것이 아닙니다.")]
    cw, gap = 3.6, 0.42
    for i, (tag, q, b) in enumerate(steps):
        x = ML + i * (cw + gap)
        rrect(s, x, y + 0.28, cw, 2.35, fill="tintblue" if i == 2 else "tint",
              line=None if i == 2 else "line", radius=0.1)
        txt(s, x + 0.32, y + 0.52, cw - 0.64, 0.3, tag, size=12, bold=True,
            color="blue" if i == 2 else "mute")
        txt(s, x + 0.32, y + 0.9, cw - 0.64, 0.5, q, size=17, bold=True, color="ink", spacing=1.15)
        txt(s, x + 0.32, y + 1.62, cw - 0.64, 0.8, b.split("\n"), size=13, color="body", spacing=1.35)
        if i < 2:
            arrow(s, x + cw + 0.05, y + 1.28, 0.32, 0.26, fill="line")
    rrect(s, ML, y + 2.95, CW, 1.2, fill="tintteal", line=None, radius=0.1)
    rich(s, ML + 0.4, y + 3.16, CW - 0.8, 0.75,
         [[("매일 쓰는 아이는 아직 많지 않습니다. ", "body", False),
           ("초등 4~6학년 중 ‘매일 이용’은 3.7%", "teal", True),
           ("입니다.", "body", False)],
          [("막아야 할 때라기보다, 습관이 굳기 전에 쓰는 방식을 정해 둘 시기입니다.",
            "body", False)]],
         size=14.5, spacing=1.35, space_after=4)
    footer(s, 24, SRC_KPF, link=URL_KPF)
    notes(s, "‘사용 시간’보다 ‘사용 방식’을 다루는 장입니다. 시간 제한만으로는 습관이 바뀌지 않습니다.\n"
             "수치 안내: 같은 조사에서 매일 이용 비율은 초등 3.7%, 중학 7.5%, 고등 15.3%입니다. "
             "학년이 올라갈수록 늘어나므로, 초등 시기가 기준을 세우기 좋은 때라고 연결해 주십시오.\n"
             "사용 시간과 종료 시점은 정답이 없습니다. 가정 상황에 맞게 아이와 함께 정하도록 안내합니다.")
    return s


def s23(prs):
    s = blank(prs)
    y = title(s, "AI가 출처를 달면 믿어도 될까요?", kicker="사실 확인 · 할루시네이션",
              sub="사실이 아닌 내용을 그럴듯하게 지어내는 일이 있습니다. 네 가지로 걸러 냅니다.")
    steps = [("링크가 실제로 열리나?", ["존재하지 않는 주소를", "만들어 내기도 합니다."]),
             ("원문에 그 내용이 있나?", ["링크는 진짜인데 내용은", "다르게 요약되기도 합니다."]),
             ("날짜와 대상이 맞나?", ["오래된 자료이거나", "다른 나라 이야기일 수 있습니다."]),
             ("반대로 물어보기", ["“틀렸다고 치고", "반박해 줘”라고", "시켜 보세요."])]
    cw = (CW - 3 * 0.3) / 4
    for i, (h, b) in enumerate(steps):
        x = ML + i * (cw + 0.3)
        last = (i == 3)
        rrect(s, x, y + 0.28, cw, 2.15, fill="tintblue" if last else "tint",
              line=None if last else "line", radius=0.1)
        numbadge(s, x + 0.3, y + 0.52, 0.4, i + 1, fill="blue")
        txt(s, x + 0.3, y + 1.08, cw - 0.6, 0.45, h, size=15.5, bold=True, color="ink", spacing=1.15)
        txt(s, x + 0.3, y + 1.55, cw - 0.6, 0.8, b, size=12, color="body", spacing=1.3)
    rrect(s, ML, y + 2.56, CW, 1.0, fill="ink", line=None, radius=0.1)
    txt(s, ML, y + 2.74, CW, 0.32,
        "아이에게 심어 줄 한 문장 — “AI는 아는 척을 아주 잘한다.”",
        size=16.5, bold=True, color="white", align=PP_ALIGN.CENTER)
    txt(s, ML, y + 3.14, CW, 0.3,
        "같은 AI에게 “정말 맞아?”라고 되묻는 것은 검증이 아닙니다. 4번처럼 반박을 시켜 보세요.",
        size=12.5, color="white", align=PP_ALIGN.CENTER)
    rrect(s, ML, y + 3.7, CW, 1.0, fill="tintteal", line=None, radius=0.1)
    rich(s, ML + 0.4, y + 3.88, CW - 0.8, 0.7,
         [[("중·고등학생의 ", "body", False), ("39%가 AI 답변을 신뢰", "teal", True),
           ("한다고 답했지만, ", "body", False),
           ("능동적으로 검증한다는 응답은 21.2%", "teal", True), ("였습니다.", "body", False)],
          [("초등학생은 이 조사의 대상이 아닙니다. 다만 확인하는 습관은 초등 시기에 자리 잡습니다.",
            "body", False)]],
         size=14.5, spacing=1.35, space_after=4)
    footer(s, 0, SRC_NYPI, link=URL_NYPI)
    notes(s, "‘AI는 거짓말을 한다’보다 ‘AI는 모르면 그럴듯하게 채운다’가 정확한 표현입니다(5장과 연결). "
             "이것을 할루시네이션이라고 부른다고 여기서 한 번 짚어 주세요.\n"
             "1~3번은 출처를 확인하는 절차입니다. 링크가 열리는지, 원문에 정말 그 내용이 있는지, "
             "날짜와 대상이 우리 상황과 맞는지 순서로 봅니다.\n"
             "4번이 새로운 기술입니다. 같은 AI에게 “정말 맞아?”라고 되묻는 것은 검증이 아닙니다. "
             "대개 “죄송합니다”라며 말을 바꿀 뿐입니다. 대신 “방금 답이 틀렸다고 가정하고 반박해 줘”라고 "
             "시켜 보십시오. 근거가 탄탄하면 반박이 궁색하고, 근거가 약했으면 순순히 말을 바꿉니다. "
             "그 반응 자체가 신호입니다.\n"
             "수치 안내: 한국청소년정책연구원 조사에서 ‘정보가 사실인지 확인할 수 있다’는 자기 평가는 "
             "3.36점, ‘편향 여부를 판단할 수 있다’는 3.45점으로 낮았습니다. 학업 성취도가 낮을수록 "
             "허위 정보를 구분하기 어려워하는 경향도 보고되었습니다.\n"
             "주의: 특정 모델의 오류율을 모든 AI의 특성처럼 말하지 않도록 합니다.")
    return s


def s24(prs):
    s = blank(prs)
    y = title(s, "사실 확인 탐정이 되어봅시다", kicker="활동 · 오류 찾기",
              sub="아래는 AI가 내놓은 답변이라고 가정한 예시입니다. 수상한 곳 네 군데를 찾아보세요.")
    rrect(s, ML, y + 0.3, 7.5, 2.75, fill="tint", line="line", radius=0.1)
    rrect(s, ML + 0.3, y + 0.5, 2.9, 0.34, fill="redbg", line=None, radius=0.3)
    txt(s, ML + 0.3, y + 0.56, 2.9, 0.3, "강사가 만든 가상 예시", size=11.5, bold=True,
        color="red", align=PP_ALIGN.CENTER)
    txt(s, ML + 0.4, y + 1.02, 6.7, 1.9,
        ["우리나라 초등학생의 스마트폰 보유율은 정확히 87.3%입니다.",
         "이는 모든 전문가가 동의하는 수치이며, 앞으로도 계속 늘어날 것이 확실합니다.",
         "(출처: 한국인터넷진흥원 「2024 청소년 스마트폰 백서」)"],
        size=15, color="ink", spacing=1.5, space_after=6)
    x = ML + 7.9
    cw = CW - 7.9
    txt(s, x, y + 0.3, cw, 0.3, "찾아야 할 네 가지", size=13, bold=True, color="teal")
    clues = ["‘정확히 87.3%’ — 지나치게 구체적인 수치",
             "‘모든 전문가가 동의’ — 단정 표현",
             "‘계속 늘어날 것이 확실’ — 예측을 사실처럼",
             "보고서 이름 — 실제로 있는지 확인 필요"]
    for i, c in enumerate(clues):
        yy = y + 0.72 + i * 0.6
        numbadge(s, x, yy, 0.32, i + 1, fill="blue", size=12)
        txt(s, x + 0.46, yy + 0.02, cw - 0.46, 0.5, c, size=13, color="body", spacing=1.25)
    rrect(s, ML, y + 3.25, CW, 1.15, fill="tintteal", line=None, radius=0.1)
    rich(s, ML + 0.4, y + 3.46, CW - 0.8, 0.7,
         [[("집에서 쓰는 한 문장: ", "body", False),
           ("“이거 어디서 나온 이야기야? 같이 찾아보자.”", "teal", True)],
          [("추궁하는 말투가 되지 않게, 같이 해보자는 쪽으로 건네 주세요.", "body", False)]],
         size=14.5, spacing=1.35, space_after=4)
    footer(s, 26, "이 답변은 활동을 위해 강사가 만든 가상 예시입니다. 실제 조사 결과가 아닙니다.")
    notes(s, "중요: 이 답변은 활동을 위해 강사가 만든 가상의 예시입니다. 실제 조사 결과가 아니며, "
             "인용하거나 배포 자료에 사실처럼 옮기지 않도록 슬라이드에서 분명히 말해 주십시오.\n"
             "진행 방법: 2분간 짝과 찾게 한 뒤 하나씩 공개합니다. 네 가지 단서는 실제 AI 답변에서도 "
             "가장 자주 나타나는 신호입니다.\n"
             "마무리 한 줄: 숫자가 구체적일수록, 표현이 단정적일수록 오히려 확인이 필요합니다.")
    return s


def s25(prs):
    s = blank(prs)
    y = title(s, "질문하기 전에 가릴 것", kicker="개인정보 보호",
              sub="한 번 입력한 내용은 되돌리기 어렵습니다.")
    items = ["이름", "학교·학년·반", "연락처", "집 주소·위치", "얼굴 사진", "친구·가족 정보"]
    cw = (CW - 2 * 0.3) / 3
    for i, it in enumerate(items):
        x = ML + (i % 3) * (cw + 0.3)
        yy = y + 0.28 + (i // 3) * 0.95
        rrect(s, x, yy, cw, 0.78, fill="redbg", line=None, radius=0.12)
        oval(s, x + 0.3, yy + 0.24, 0.3, 0.3, fill="red")
        txt(s, x + 0.78, yy + 0.22, cw - 1.0, 0.35, it, size=16, bold=True, color="ink")
    rrect(s, ML, y + 2.3, CW, 1.05, fill="tint", line="line", radius=0.1)
    txt(s, ML + 0.4, y + 2.5, 5.0, 0.3, "이렇게 바꿔서 물어봅니다", size=13, bold=True, color="teal")
    rich(s, ML + 0.4, y + 2.88, CW - 0.8, 0.4,
         [[("“김○○이 서울○○초 4학년인데…” ", "mute", False), ("→  ", "blue", True),
           ("“초등학교 4학년 학생인데…”", "ink", True)]], size=15.5)
    rrect(s, ML, y + 3.5, CW, 1.2, fill="tintteal", line=None, radius=0.1)
    rich(s, ML + 0.4, y + 3.7, CW - 0.8, 0.9,
         [[("학교 평가 지침에도 개인정보 보호가 따로 들어가 있습니다.", "teal", True)],
          [("과제에 AI를 쓸 때 무엇을 입력했는지까지 보도록 되어 있습니다. "
            "집에서도 같은 기준이면 아이가 헷갈리지 않습니다.", "body", False)]],
         size=14.5, spacing=1.35, space_after=4)
    footer(s, 27, SRC_MOE, link=URL_MOE)
    notes(s, "‘가짜 이름으로 바꾸기’는 아이가 바로 따라 할 수 있는 기술입니다. 실제로 한 번 시연해 주십시오.\n"
             "덧붙일 내용: 사진에는 교복, 아파트 동호수, 학교 이름표 같은 정보가 함께 담기는 경우가 많습니다. "
             "친구의 글이나 사진을 올리는 것은 다른 사람의 정보를 내가 입력하는 일이라는 점도 짚어 주십시오.\n"
             "서비스 설정에서 대화 내용을 학습에 사용하지 않도록 선택할 수 있는 경우가 있으나, "
             "서비스와 계정 유형마다 다르므로 각자 확인이 필요하다고만 안내합니다.")
    return s


def s26(prs):
    s = blank(prs)
    y = title(s, "도구는 아래층부터 쌓아야 합니다", kicker="준비시킬 것",
              sub="AI는 맨 위에 올라가는 층입니다. 아래가 비어 있으면 올릴 자리가 없습니다.")
    cxc = ML + 3.85
    rrect(s, cxc - 1.65, y + 0.2, 3.3, 0.6, fill="blue", line=None, radius=0.12)
    txt(s, cxc - 1.65, y + 0.34, 3.3, 0.35, "AI", size=17, bold=True, color="white",
        align=PP_ALIGN.CENTER)
    layers = [("3층  표현", "초 5~6학년 · 슬라이드, 짧은 영상 편집, 발표",
               4.9, "tintteal", "ink", None),
              ("2층  정리", "초 5학년~ · 표 만들기 기초(합계·차트), 마인드맵",
               6.2, "teal", "white", None),
              ("1층  기록", "초 3학년~ · 한글 자판, 메모 앱, 사진과 파일 정리",
               7.5, "ink", "white", None)]
    for i, (name, body, w, bg, fg, _) in enumerate(layers):
        ly = y + 0.88 + i * 0.94
        rrect(s, cxc - w / 2, ly, w, 0.88, fill=bg, line=None, radius=0.06)
        txt(s, cxc - w / 2 + 0.3, ly + 0.14, w - 0.6, 0.3, name, size=15, bold=True, color=fg)
        txt(s, cxc - w / 2 + 0.3, ly + 0.48, w - 0.6, 0.3, body, size=11.5, color=fg)

    bx = ML + 7.9
    bw = CW - 7.9
    rrect(s, bx, y + 0.2, bw, 3.5, fill="tint", line="line", radius=0.1)
    txt(s, bx + 0.32, y + 0.45, bw - 0.64, 0.3, "가장 과소평가된 기술", size=12,
        bold=True, color="teal")
    txt(s, bx + 0.32, y + 0.82, bw - 0.64, 0.4, "타자와 검색어 만들기", size=17,
        bold=True, color="ink")
    txt(s, bx + 0.32, y + 1.32, bw - 0.64, 0.9,
        ["궁금한 것을 짧은 문장으로", "옮기는 힘이 곧 프롬프트", "실력이 됩니다."],
        size=13, color="body", spacing=1.35)
    rect(s, bx + 0.32, y + 2.35, bw - 0.64, 0.012, fill="line")
    txt(s, bx + 0.32, y + 2.55, bw - 0.64, 0.3, "모든 층에 걸치는 두 가지", size=12,
        bold=True, color="teal")
    txt(s, bx + 0.32, y + 2.88, bw - 0.64, 0.6,
        ["· 출처 표시하기", "· 개인정보 관리하기"], size=13.5, color="ink", spacing=1.35)

    rrect(s, ML, y + 3.88, CW, 0.82, fill="tintteal", line=None, radius=0.1)
    txt(s, ML + 0.4, y + 4.08, CW - 0.8, 0.45,
        "1층이 부실한 채로 AI만 얹으면, 아이는 결과만 받고 과정을 잃습니다.",
        size=15.5, bold=True, color="teal")
    footer(s, 0)
    notes(s, "‘우리 아이만 뒤처지는 것 아닌가’와 ‘몇 학년에 뭘 가르쳐야 하나’에 한꺼번에 답하는 장입니다.\n"
             "순서가 핵심입니다. 1층 기록(타자, 메모, 파일 정리)이 되어야 2층 정리(표, 마인드맵)가 되고, "
             "그래야 3층 표현(슬라이드, 영상, 발표)이 가능합니다. AI는 그 위에 얹히는 지붕입니다. "
             "학년 표기는 참고용이며 아이마다 다릅니다.\n"
             "오른쪽 상자를 강조해 주세요. 타자와 검색어 만들기는 학원에서 안 가르치지만 가장 오래 쓰입니다. "
             "특히 검색어를 만드는 일은 ‘내가 무엇을 모르는지 한 문장으로 말하기’와 같고, "
             "그게 곧 27장에서 배운 프롬프트 공식입니다.\n"
             "출처 표시와 개인정보 관리는 어느 한 층의 기술이 아니라 모든 층에 걸칩니다. "
             "1층에서 사진을 정리할 때부터 시작되는 습관이라고 말씀해 주세요.\n"
             "특정 AI 제품 사용법을 일찍 배우는 것이 경쟁력이 되지는 않는다는 점, 그러나 "
             "‘그러니 아무것도 안 해도 된다’로 들리지 않게 균형을 잡아 주십시오.")
    return s


def s27(prs):
    s = blank(prs)
    y = title(s, "아이가 보여준 이상한 답변, 어떻게 반응할까요?", kicker="문제가 생겼을 때",
              sub="무섭거나 불쾌한 내용을 만났을 때의 순서입니다.")
    steps = [("닫기", "그 화면을 바로 닫습니다.\n계속 보거나 되묻지 않습니다.", "blue"),
             ("알리기", "보호자에게 말합니다.\n“말해 줘서 고맙다”가 첫마디입니다.", "blue"),
             ("함께 확인하기", "무슨 일이 있었는지 같이 보고\n필요하면 신고·차단·설정을 바꿉니다.", "teal")]
    cw, gap = 3.6, 0.42
    for i, (h, b, col) in enumerate(steps):
        x = ML + i * (cw + gap)
        rrect(s, x, y + 0.28, cw, 2.2, fill="tintblue" if i < 2 else "tintteal",
              line=None, radius=0.1)
        numbadge(s, x + 0.32, y + 0.52, 0.42, i + 1, fill=col)
        txt(s, x + 0.32, y + 1.08, cw - 0.64, 0.4, h, size=18, bold=True, color="ink")
        txt(s, x + 0.32, y + 1.58, cw - 0.64, 0.75, b.split("\n"), size=13, color="body", spacing=1.35)
        if i < 2:
            arrow(s, x + cw + 0.05, y + 1.22, 0.32, 0.26, fill="line")
    rrect(s, ML, y + 2.78, CW, 1.45, fill="tint", line="line", radius=0.1)
    rich(s, ML + 0.4, y + 3.0, CW - 0.8, 0.95,
         [[("혼내면 다음부터 말하지 않습니다.", "red", True)],
          [("아이가 화면을 들고 왔다면, 그건 부모를 믿고 있다는 뜻입니다.", "body", False)],
          [("“잘 닫았네. 보여 줘서 고마워.” 이 한마디가 다음 신고를 만듭니다.", "ink", True)]],
         size=14.5, spacing=1.35, space_after=5)
    footer(s, 29, "참고: OpenAI 자녀 보호 기능 안내 (신고·차단·보호자 설정)", link=URL_OPENAI_PC)
    notes(s, "실제로 가장 많이 어긋나는 지점입니다. 놀란 부모가 먼저 화를 내면 아이는 다음부터 숨깁니다.\n"
             "서비스별로 신고 기능과 보호자 관리 기능이 있고, 계정 연결로 사용 시간대나 기능을 제한할 수 있는 "
             "경우도 있습니다(14장). 다만 기능은 자주 바뀌므로 각자 확인이 필요하다고 안내합니다.\n"
             "심각한 내용(자해·성적 대화·협박 등)이라면 담임 교사, 학교 상담 선생님과 상의하도록 권합니다.")
    return s


def s28(prs):
    s = blank(prs)
    y = title(s, "우리 집 AI 사용 약속", kicker="활동 · 가족 규칙 작성",
              sub="빈칸을 채워서 한 장 들고 가세요.")
    lines = ["우리는 AI를 ____________________ 할 때 사용한다.",
             "사용하기 전에는 먼저 ____________________ 한다.",
             "숙제에서는 선생님의 ____________________ 을 확인한다.",
             "____________________ 정보는 입력하지 않는다.",
             "사용한 뒤에는 ____________________ 을 내 말로 설명한다.",
             "이상한 답이 나오면 ____________________ 한다."]
    rrect(s, ML, y + 0.25, 7.55, 4.1, fill="tint", line="line", radius=0.1)
    for i, ln in enumerate(lines):
        yy = y + 0.55 + i * 0.62
        numbadge(s, ML + 0.35, yy + 0.02, 0.32, i + 1, fill="teal", size=12)
        txt(s, ML + 0.82, yy, 6.6, 0.4, ln, size=15, color="ink")
    x = ML + 7.95
    cw = CW - 7.95
    rrect(s, x, y + 0.25, cw, 4.1, fill="tintblue", line=None, radius=0.1)
    txt(s, x + 0.32, y + 0.52, cw - 0.64, 0.3, "채우기 어려우면 이렇게", size=13, bold=True, color="blue")
    hints = ["① 모르는 낱말을 알아볼 때",
             "② 내가 아는 것을 한 가지 말할 때",
             "③ 과제 지침",
             "④ 이름·학교·주소·사진",
             "⑤ 오늘 알게 된 것",
             "⑥ 화면을 닫고 부모에게 말"]
    txt(s, x + 0.32, y + 1.0, cw - 0.64, 3.0, hints, size=13.5, color="body",
        spacing=1.35, space_after=9)
    footer(s, 30)
    notes(s, "8~10분 활동입니다. 유인물로 나눠 드리고 직접 쓰게 하십시오. 완성본을 냉장고에 붙이도록 권합니다.\n"
             "진행 요령: 모두 채우려 하지 말고 오늘 정할 수 있는 두세 칸만 채우게 합니다. "
             "나머지는 집에 가서 아이와 함께 채우는 것이 더 좋습니다. 아이가 직접 쓴 규칙이 훨씬 오래 갑니다.\n"
             "1~2 가정에서 발표를 받으면 마무리가 자연스럽습니다.")
    return s


def s29(prs):
    s = blank(prs)
    y = title(s, "학부모 질문, 한 장으로 정리", kicker="요약",
              sub="오늘 나온 질문을 한 장에 모았습니다.")
    qa = [("시작 나이", "하나의 나이는 없습니다.\n서비스 조건 → 학교 지침 → 아이의 준비도 순으로 봅니다."),
          ("부모 휴대폰", "처음에는 함께 씁니다.\n무엇을 알아볼지, 무엇을 넣을지, 언제 끝낼지를 먼저 정합니다."),
          ("책·검색보다 먼저?", "AI는 세 번째 자리입니다.\n내 생각 → 자료 찾기 다음에 놓습니다."),
          ("숙제", "교사의 과제 지침이 먼저입니다.\n설명·힌트·피드백은 되고, 작성 대행은 안 됩니다."),
          ("자주 찾는 아이", "쓰기 전 “네 생각은?”,\n쓴 뒤 “닫고 설명해 볼까?”를 붙입니다."),
          ("사실 확인", "출처를 요청한 뒤 원문을 엽니다.\n같은 AI에게 되묻는 것은 검증이 아닙니다.")]
    cw = (CW - 2 * 0.3) / 3
    for i, (q, a) in enumerate(qa):
        x = ML + (i % 3) * (cw + 0.3)
        yy = y + 0.28 + (i // 3) * 2.1
        rrect(s, x, yy, cw, 1.9, fill="tint", line="line", radius=0.1)
        rect(s, x + 0.28, yy + 0.3, 0.4, 0.05, fill="blue")
        txt(s, x + 0.28, yy + 0.52, cw - 0.56, 0.35, q, size=16.5, bold=True, color="ink")
        txt(s, x + 0.28, yy + 1.0, cw - 0.56, 0.8, a.split("\n"), size=13, color="body", spacing=1.35)
    footer(s, 31)
    notes(s, "질의응답 시간에 띄워 두는 장입니다. 질문이 나오면 해당 칸을 짚으며 답하면 됩니다.\n"
             "답을 모르는 질문이 나오면 추측하지 말고 ‘확인해서 알려 드리겠다’고 하십시오. "
             "특히 특정 서비스의 최신 약관, 우리 학교의 구체적 지침은 그 자리에서 단정하지 않는 편이 안전합니다.")
    return s


def s30(prs):
    s = blank(prs)
    rect(s, 0, 0, W, 0.16, fill="blue")
    txt(s, ML, 1.35, CW, 0.3, "오늘부터", size=14, bold=True, color="teal", align=PP_ALIGN.CENTER)
    txt(s, ML, 1.78, CW, 0.7, "한 문장만 바꿔 주세요", size=34, bold=True, color="ink",
        align=PP_ALIGN.CENTER)
    bw = 4.55
    x1 = (W - (bw * 2 + 1.0)) / 2
    rrect(s, x1, 3.0, bw, 1.25, fill="tint", line="line", radius=0.12)
    txt(s, x1, 3.45, bw, 0.45, "“AI가 뭐라고 했어?”", size=19, color="mute", align=PP_ALIGN.CENTER)
    arrow(s, x1 + bw + 0.28, 3.47, 0.45, 0.3, fill="blue")
    rrect(s, x1 + bw + 1.0, 3.0, bw, 1.25, fill="tintblue", line=None, radius=0.12)
    txt(s, x1 + bw + 1.0, 3.45, bw, 0.45, "“너는 어떻게 생각해?”", size=19, bold=True,
        color="ink", align=PP_ALIGN.CENTER)
    txt(s, ML, 4.85, CW, 0.4,
        "AI를 막는다고 아이의 생각이 지켜지지는 않습니다.",
        size=16, color="body", align=PP_ALIGN.CENTER)
    txt(s, ML, 5.3, CW, 0.4,
        "먼저 묻고, 같이 확인하고, 자기 말로 설명하게 해 주세요.",
        size=16, color="body", align=PP_ALIGN.CENTER)
    rrect(s, (W - 5.4) / 2, 6.05, 5.4, 0.58, fill="tintteal", line=None, radius=0.3)
    txt(s, (W - 5.4) / 2, 6.22, 5.4, 0.3, "오늘 실천할 한 가지를 정해 주세요.",
        size=14.5, bold=True, color="teal", align=PP_ALIGN.CENTER)
    notes(s, "마무리입니다. 참석자에게 오늘 배운 것 중 ‘집에 가서 바로 할 한 가지’를 마음속으로 정하게 하고, "
             "원한다면 한두 분께 말로 표현하게 합니다.\n"
             "가장 많이 선택되는 것: ①쓰기 전 ‘네 생각은?’ 묻기 ②화면 닫고 설명하게 하기 "
             "③‘정답 말고 힌트만’ 문장 알려 주기 ④신호등 만들기.\n"
             "연수 자료와 유인물(약속 양식, 프롬프트 예시)을 어디서 받을 수 있는지 안내하고 마칩니다.")
    return s
