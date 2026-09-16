# -*- coding: utf-8 -*-
"""슬라이드 11~20"""
from deckkit import *
from slides_a import SRC_KPF, SRC_PNAS, SRC_MOE, SRC_NYPI, URL_PNAS, URL_MOE
from pptx.enum.text import PP_ALIGN

SRC_CURR = "출처: 교육부, 2022 개정 교육과정(정보 교육 시수 확대) — 국가교육과정정보센터"
URL_CURR = "https://ncic.re.kr/"
URL_OPENAI = "https://help.openai.com/en/articles/8313401-is-chatgpt-safe-for-all-ages"
URL_OPENAI_PC = "https://help.openai.com/en/articles/12315553"
URL_GEMINI = "https://support.google.com/families/answer/16109150?hl=ko"
URL_CLAUDE = ("https://support.claude.com/en/articles/"
              "13117299-minimum-age-requirement-access-restriction")
URL_COPILOT = ("https://support.microsoft.com/en-us/microsoft-copilot/"
               "microsoft-copilot-age-limits-and-parental-controls")
URL_PPLX = "https://www.perplexity.ai/hub/legal/terms-of-service"
URL_WRTN = "https://help.wrtn.ai/account_14"
URL_TOCTOC = "https://www.toctocmath.kr/"
URL_PENGTALK = "https://about.ebs.co.kr/kor/elearning/grade?tabVal=aipengtalk"
URL_PRIVACY = "https://www.privacy.go.kr/front/contents/cntntsView.do?contsNo=94"
SRC_TOS = ("출처: OpenAI 고객센터·이용약관, Google Gemini/Family Link 고객센터 (2026년 9월 확인 기준) · "
           "개인정보 보호법 제22조의2(아동의 개인정보 보호)")


def s11(prs):
    s = blank(prs)
    y = title(s, "학교에서는 어떤 AI를 쓰나요?", kicker="학교의 AI 교육",
              sub="학교에서 말하는 AI 교육에는 세 갈래가 있습니다.")
    items = [("AI 원리 배우기", "AI가 무엇이고 어떻게 작동하는지\n배웁니다. 정보·실과 수업이\n여기에 해당합니다.", "teal"),
             ("AI로 학습하기", "수업이나 과제에서 도구로\n활용합니다. 교사가 범위를 정해\n안내합니다.", "blue"),
             ("AI를 비판적으로 살피기", "편향·오류·개인정보를 따져 봅니다.\n오늘 가정에서 함께할 부분이\n바로 이것입니다.", "blue")]
    cw, gap = 3.6, 0.42
    for i, (h, b, col) in enumerate(items):
        x = ML + i * (cw + gap)
        rrect(s, x, y + 0.28, cw, 2.35, fill="tint" if i < 2 else "tintblue",
              line="line" if i < 2 else None, radius=0.1)
        rect(s, x + 0.32, y + 0.58, 0.45, 0.05, fill=col)
        txt(s, x + 0.32, y + 0.82, cw - 0.64, 0.45, h, size=17.5, bold=True, color="ink", spacing=1.15)
        txt(s, x + 0.32, y + 1.38, cw - 0.64, 1.0, b.split("\n"), size=13, color="body", spacing=1.35)
    rrect(s, ML, y + 2.98, CW, 1.35, fill="tintteal", line=None, radius=0.1)
    rich(s, ML + 0.4, y + 3.14, CW - 0.8, 1.1,
         [[("2022 개정 교육과정에서 초등학교 정보 교육이 17시간에서 ", "body", False),
           ("34시간 이상", "teal", True),
           ("으로 늘었습니다(중학교는 68시간 이상).", "body", False)],
          [("초등 5·6학년은 2026년 3월부터 적용되며, 실과 정보 영역과 학교 자율시간 등으로 편성합니다.",
            "body", False)],
          [("학교가 손 놓고 있는 분야가 아니라, 이미 교육과정 안에 들어와 있는 내용입니다.", "body", False)]],
         size=14, spacing=1.35, space_after=3)
    footer(s, 11, SRC_CURR, link=URL_CURR)
    notes(s, "학부모가 ‘학교는 뭘 하고 있나’라고 묻는 지점입니다. 세 갈래를 구분해 주면 오해가 줄어듭니다.\n"
             "시수 안내: 2022 개정 교육과정에서 초등 정보 교육은 실과 내 17시간에서 34시간 이상으로, "
             "중학교 정보는 34시간에서 68시간 이상으로 확대되었습니다. 학교마다 편성 방식(학교 자율시간 활용 등)이 "
             "다르므로, 우리 학교의 실제 운영은 다음 장의 체크리스트로 확인하도록 안내합니다.\n"
             "주의: 개별 학교의 도입률이나 특정 사업 참여 학교 수는 확인된 자료가 아니면 말하지 않습니다.")
    return s


def s12(prs):
    s = blank(prs)
    y = title(s, "우리 학교에 확인할 네 가지", kicker="학부모 체크리스트",
              sub="상담 주간이나 알림장으로 물어보실 수 있는 질문입니다.")
    items = [("사용 도구", "“수업에서 어떤 AI 서비스를 쓰나요?”",
              "제품 이름과 학생 계정 사용 여부"),
             ("계정·개인정보", "“학생 계정은 어떻게 만들고 관리하나요?”",
              "교육용 계정인지, 입력 정보는 무엇인지"),
             ("과제 허용 범위", "“과제에서 AI는 어디까지 되나요?”",
              "과목·과제 유형별로 다를 수 있음"),
             ("평가 기준", "“AI를 쓰면 표기해야 하나요?”",
              "표기 방법과 위반 시 처리 기준")]
    cw, gap = (CW - 0.4) / 2, 0.4
    for i, (h, q, b) in enumerate(items):
        x = ML + (i % 2) * (cw + gap)
        yy = y + 0.28 + (i // 2) * 1.68
        rrect(s, x, yy, cw, 1.48, fill="tint", line="line", radius=0.1)
        numbadge(s, x + 0.32, yy + 0.3, 0.42, i + 1, fill="blue")
        txt(s, x + 0.98, yy + 0.28, cw - 1.3, 0.35, h, size=16.5, bold=True, color="ink")
        txt(s, x + 0.98, yy + 0.68, cw - 1.3, 0.35, q, size=14, color="blue")
        txt(s, x + 0.98, yy + 1.04, cw - 1.3, 0.35, b, size=12, color="mute")
    rrect(s, ML, y + 3.72, CW, 0.78, fill="tintblue", line=None, radius=0.12)
    txt(s, ML + 0.4, y + 3.93, CW - 0.8, 0.4,
        "이 네 가지만 알고 계시면 집에서 정할 규칙도 자연스럽게 잡힙니다.",
        size=15.5, bold=True, color="blue")
    footer(s, 12)
    notes(s, "이 장은 사진을 찍어 가시라고 안내하면 좋습니다.\n"
             "따지려는 질문이 아니라 ‘가정에서 같은 기준을 쓰기 위해서’ 묻는 것이라는 태도를 강조해 주십시오. "
             "특히 세 번째와 네 번째는 학년·과목마다 다를 수 있으므로 담임 선생님께 확인하는 것이 정확합니다.")
    return s


def s13(prs):
    s = blank(prs)
    y = title(s, "부모 휴대폰, 어디까지 빌려줄까요?", kicker="첫 번째 관문 · 이용 조건",
              sub="빌려주기 전에, 그 서비스가 정해 둔 조건부터 보셔야 합니다.")
    cw = (CW - 0.4) / 2
    card(s, ML, y + 0.15, cw, 1.88, "보호자와 함께 쓰기",
         ["· 무엇을 알아볼지 먼저 정합니다",
          "· 어떤 정보를 넣을지 함께 봅니다",
          "· 언제 끝낼지 미리 약속합니다"],
         fill="tintblue", line=None, accent="blue", head_size=17.5, body_size=13)
    card(s, ML + cw + 0.4, y + 0.15, cw, 1.88, "아이 혼자 쓰기",
         ["· 10장의 준비도 네 가지를 갖췄을 때",
          "· 사용 목적과 시간을 정해 둔 상태에서",
          "· 무엇을 물었는지 나중에 이야기하기로"],
         fill="tint", line="line", accent="teal", head_size=17.5, body_size=13)

    ty = y + 2.16
    rrect(s, ML, ty, CW, 1.48, fill="tint", line="line", radius=0.08)
    rect(s, ML, ty, CW, 0.44, fill="tintteal")
    cols = [0.35, 2.85, 6.35]
    heads = ["서비스", "연령·동의 조건", "보호자가 할 수 있는 것"]
    for cx, hd in zip(cols, heads):
        txt(s, ML + cx, ty + 0.12, 3.6, 0.3, hd, size=12.5, bold=True, color="teal")
    rows = [("ChatGPT (OpenAI)", "만 13세 미만 이용 불가.\n13~18세는 보호자 동의 필요.",
             "(13세 이상) 자녀 계정과 연결해\n사용 금지 시간대·기능 제한, 대화 내용 열람은 불가"),
            ("Gemini (Google)", "만 13세 미만(국내 만 14세)은\n보호자가 Family Link로 관리",
             "Family Link에서 액세스를 켜고 끄기")]
    for i, (a, b, c) in enumerate(rows):
        ry = ty + 0.5 + i * 0.52
        txt(s, ML + cols[0], ry, 2.4, 0.3, a, size=13, bold=True, color="blue",
            link=(URL_OPENAI_PC if i == 0 else URL_GEMINI), underline=True)
        txt(s, ML + cols[1], ry - 0.06, 3.3, 0.55, b.split("\n"), size=12, color="body", spacing=1.25)
        txt(s, ML + cols[2], ry - 0.06, 4.9, 0.55, c.split("\n"), size=12, color="body", spacing=1.25)
    rrect(s, ML, y + 3.78, CW, 0.92, fill="tintteal", line=None, radius=0.12)
    rich(s, ML + 0.4, y + 3.97, CW - 0.8, 0.6,
         [[("국내에서는 만 14세 미만 아동의 서비스 가입에 보호자 동의가 필요합니다. "
            "초등 단계는 동반 사용이 기본입니다.", "teal", True)],
          [("연령·계정 정책은 자주 바뀝니다. 실제로 쓰실 서비스의 공식 약관과 도움말을 확인해 주세요.",
            "body", False)]],
         size=13.5, spacing=1.35, space_after=3)
    footer(s, 13, SRC_TOS, link=URL_PRIVACY)
    notes(s, "표의 내용은 2026년 9월 확인 기준이며, 정책은 자주 바뀝니다. 연수 직전에 다시 확인하시고 "
             "바뀐 부분이 있으면 구두로 정정해 주십시오.\n"
             "핵심 메시지: ①일반 소비자용 서비스와 학교가 제공하는 교육용 계정은 조건이 다릅니다. "
             "②부모 계정을 그냥 빌려주는 방식은 서비스가 정한 연령·계정 공유 조건을 벗어날 수 있습니다. "
             "③‘보호자 동의’는 서류상 동의가 아니라 함께 쓰는 실제 습관을 뜻한다고 풀어 주십시오.\n"
             "‘자녀 계정 연결’ 질문이 나오면: 부모 계정과 아이 본인 계정을 묶는 기능이며, "
             "아이가 이미 자기 계정을 가지고 있어야 합니다(만 13~18세). 부모가 설정 → 자녀 보호 기능 → "
             "가족 구성원 추가에서 전화번호나 이메일로 초대하면 아이가 링크를 눌러 수락합니다. "
             "연결하면 사용 금지 시간대(Quiet hours), 음성 모드·이미지 생성·메모리 끄기, 민감 콘텐츠 제한을 "
             "부모가 정할 수 있고, 연결된 동안 아이는 이 설정을 바꿀 수 없습니다.\n"
             "다만 부모가 아이의 대화 내용을 읽을 수는 없습니다. 학부모가 가장 많이 오해하는 지점이므로 "
             "먼저 짚어 주십시오. 감시 도구가 아니라 사용 조건을 거는 도구입니다.\n"
             "초등학교 학부모에게는 아직 해당하지 않는 기능입니다. 13세 미만은 계정 자체를 만들 수 없으므로 "
             "지금은 보호자 동반 사용이 기본이고, 중학교에 올라가면 쓸 수 있는 기능이라고 예고하는 정도로 "
             "안내하십시오.\n"
             "특정 제품을 권하거나 비교 평가하는 자리가 아님을 분명히 하고, 두 서비스는 예시로만 제시합니다.")
    return s


def s14(prs):
    s = blank(prs)
    y = title(s, "우리 집 AI 사용 신호등", kicker="가정 기준 만들기",
              sub="세 가지 색으로 나누면 아이도 바로 이해합니다.")
    cols = [("초록", "green", "greenbg", "그냥 해도 됩니다",
             ["· 모르는 낱말·개념 설명 듣기", "· 내가 쓴 글에 대한 피드백 받기",
              "· 문제의 첫 번째 힌트만 받기", "· 아이디어를 넓히는 질문 받기"]),
            ("노랑", "amber", "amberbg", "물어보고 씁니다",
             ["· 과제·수행평가에 활용하기", "· 사진·파일을 올려서 묻기",
              "· 새로운 서비스에 가입하기", "· 긴 글을 통째로 요약하기"]),
            ("빨강", "red", "redbg", "하지 않습니다",
             ["· 이름·학교·주소·연락처 입력", "· 얼굴 사진, 친구 정보 올리기",
              "· 답안을 그대로 베껴 제출하기", "· 부모 몰래 결제하기"])]
    cw, gap = 3.6, 0.42
    for i, (name, col, bg, rule, items) in enumerate(cols):
        x = ML + i * (cw + gap)
        rrect(s, x, y + 0.28, cw, 3.55, fill=bg, line=None, radius=0.08)
        oval(s, x + 0.32, y + 0.55, 0.42, 0.42, fill=col)
        txt(s, x + 0.92, y + 0.58, 1.6, 0.35, name, size=17, bold=True, color=col)
        txt(s, x + 0.32, y + 1.18, cw - 0.64, 0.35, rule, size=16, bold=True, color="ink")
        txt(s, x + 0.32, y + 1.68, cw - 0.64, 1.9, items, size=13, color="body",
            spacing=1.3, space_after=6)
    rrect(s, ML, y + 4.0, CW, 0.68, fill="tint", line="line", radius=0.12)
    txt(s, ML + 0.4, y + 4.18, CW - 0.8, 0.4,
        "노랑 칸이 제일 중요합니다. 무조건 막기보다 “먼저 물어본다”를 습관으로 만들어 주세요.",
        size=14.5, bold=True, color="ink")
    footer(s, 15)
    notes(s, "신호등은 냉장고에 붙여 두기 좋은 형태입니다. 28장에서 각 가정이 직접 채웁니다.\n"
             "빨강은 협상하지 않는 선(개인정보·대필·결제)만 짧게 둡니다. 빨강이 길어지면 아이가 전부를 금지로 받아들입니다.\n"
             "노랑의 ‘물어본다’는 허락을 받으라는 뜻이면서, 부모가 아이의 사용을 알게 되는 통로이기도 합니다.")
    return s


def s15(prs):
    s = blank(prs)
    y = title(s, "책·검색·AI, 무엇부터 해야 할까요?", kicker="순서가 중요합니다",
              sub="AI를 먼저 켜면 아이의 첫 생각이 사라집니다.")
    steps = ["내 생각 꺼내기", "자료 찾기", "AI에게 도움 받기", "원문으로 확인하기", "내 말로 설명하기"]
    subs = ["이미 아는 것과\n궁금한 것 말하기", "책·교과서·검색으로\n사실 찾기", "어려운 부분만\n설명·힌트 요청",
            "AI가 말한 내용을\n자료와 대조", "화면을 닫고\n스스로 정리"]
    cw = 2.02
    gap = (CW - 5 * cw) / 4
    for i, (st, sb) in enumerate(zip(steps, subs)):
        x = ML + i * (cw + gap)
        hi = (i == 2)
        rrect(s, x, y + 0.5, cw, 2.15, fill="tintblue" if hi else "tint",
              line=None if hi else "line", radius=0.1)
        numbadge(s, x + cw / 2 - 0.21, y + 0.75, 0.42, i + 1, fill="blue" if hi else "teal")
        txt(s, x + 0.12, y + 1.35, cw - 0.24, 0.5, st, size=14, bold=True, color="ink",
            align=PP_ALIGN.CENTER, spacing=1.15)
        txt(s, x + 0.12, y + 1.88, cw - 0.24, 0.6, sb.split("\n"), size=11.5, color="body",
            align=PP_ALIGN.CENTER, spacing=1.25)
        if i < 4:
            arrow(s, x + cw + gap / 2 - 0.16, y + 1.42, 0.32, 0.26, fill="line")
    rrect(s, ML, y + 2.95, CW, 1.15, fill="tintteal", line=None, radius=0.1)
    rich(s, ML + 0.4, y + 3.17, CW - 0.8, 0.7,
         [[("AI는 세 번째 자리입니다. ", "teal", True),
           ("1번과 2번을 건너뛰면 아이는 뭘 모르는지도 모른 채 답부터 받습니다.", "body", False)],
          [("5번까지 가서 한 바퀴를 닫아야 그날 공부가 아이한테 남습니다.", "body", False)]],
         size=14.5, spacing=1.35, space_after=4)
    footer(s, 16)
    notes(s, "예시로 풀어 주면 좋습니다. ‘동물 조사 숙제’라면 ①내가 아는 것 말하기 → ②도감·교과서에서 사실 찾기 → "
             "③어려운 낱말을 AI에게 설명 요청 → ④찾은 사실을 자료와 대조 → ⑤자기 말로 발표 연습.\n"
             "부모가 개입할 지점은 1번과 5번입니다. 이 두 곳만 지켜도 나머지는 크게 어긋나지 않습니다.")
    return s


def s16(prs):
    s = blank(prs)
    y = title(s, "세 가지 도구는 역할이 다릅니다", kicker="도구 구분",
              sub="셋 다 필요합니다. 하는 일이 서로 다르거든요.")
    items = [("책", "맥락을 읽습니다",
              ["· 앞뒤가 이어진 긴 설명", "· 검증을 거친 내용", "· 느리지만 깊게 남음"], "teal"),
             ("검색", "원자료를 찾습니다",
              ["· 기관·언론의 원문에 접근", "· 날짜와 출처가 드러남", "· 여러 자료를 비교 가능"], "teal"),
             ("AI", "설명과 연습을 돕습니다",
              ["· 어려운 말을 쉽게 풀어 줌", "· 되묻고 힌트를 줌", "· 사실은 따로 확인해야 함"], "blue")]
    cw, gap = 3.6, 0.42
    for i, (name, role, bullets, col) in enumerate(items):
        x = ML + i * (cw + gap)
        rrect(s, x, y + 0.3, cw, 2.9, fill="tintblue" if i == 2 else "tint",
              line=None if i == 2 else "line", radius=0.1)
        txt(s, x + 0.32, y + 0.58, cw - 0.64, 0.45, name, size=24, bold=True, color=col)
        txt(s, x + 0.32, y + 1.12, cw - 0.64, 0.35, role, size=15.5, bold=True, color="ink")
        txt(s, x + 0.32, y + 1.65, cw - 0.64, 1.3, bullets, size=13, color="body",
            spacing=1.3, space_after=6)
    rrect(s, ML, y + 3.55, CW, 0.75, fill="tintteal", line=None, radius=0.12)
    txt(s, ML + 0.4, y + 3.75, CW - 0.8, 0.4,
        "AI가 책 읽기와 자료 찾기까지 가져가지 않도록 자리를 정해 주시면 됩니다.",
        size=14.5, bold=True, color="teal")
    footer(s, 17)
    notes(s, "‘AI가 다 해 주는데 왜 책을 읽어야 하나요’라는 질문에 대한 답입니다. "
             "AI는 설명은 잘하지만 그 설명이 맞는지는 보증하지 않습니다. 검색은 원문에 닿게 해 주고, "
             "책은 앞뒤 맥락을 줍니다. 셋의 기능이 겹치지 않는다는 점을 짚어 주십시오.")
    return s


def s17(prs):
    s = blank(prs)
    y = title(s, "숙제에 AI를 써도 될까요?", kicker="숙제와 평가",
              sub="정부와 교육청은 ‘일률적 금지’ 대신 ‘범위를 정해 활용’을 선택했습니다.")
    rrect(s, ML, y + 0.28, CW, 1.05, fill="tintblue", line=None, radius=0.1)
    rich(s, ML + 0.4, y + 0.5, CW - 0.8, 0.65,
         [[("교육부와 17개 시도교육청은 ", "body", False),
           ("「수행평가 시 인공지능(AI) 활용 관리 방안」", "blue", True),
           ("을 마련했습니다.", "body", False)],
          [("중·고등학교 수행평가가 중심이지만, 금지보다 안전하고 교육적으로 활용하게 한다는 "
            "방향을 보여 줍니다.", "body", False)]],
         size=14.5, spacing=1.35, space_after=4)
    areas = ["AI 활용 범위 설정", "AI 활용 과정 표기 지도", "학생 유의 사항 안내·사전교육",
             "평가 설계 방향", "개인정보 보호"]
    cw = (CW - 4 * 0.24) / 5
    for i, a in enumerate(areas):
        x = ML + i * (cw + 0.24)
        rrect(s, x, y + 1.55, cw, 1.35, fill="tint", line="line", radius=0.1)
        numbadge(s, x + cw / 2 - 0.2, y + 1.78, 0.4, i + 1, fill="teal", size=14)
        txt(s, x + 0.14, y + 2.35, cw - 0.28, 0.5, a, size=13, bold=True, color="ink",
            align=PP_ALIGN.CENTER, spacing=1.2)
    rrect(s, ML, y + 3.15, CW, 1.58, fill="tint", line="line", radius=0.1)
    txt(s, ML + 0.4, y + 3.33, 4.0, 0.3, "금지되는 행위로 제시된 예", size=13, bold=True, color="red")
    txt(s, ML + 0.4, y + 3.68, CW - 0.8, 0.6,
        ["· AI가 생성한 글·이미지를 자신의 창작물로 제출하는 행위",
         "· 문제풀이 앱 등에 평가 문항을 입력하고 생성된 답안을 그대로 제출하는 행위"],
        size=14, color="body", spacing=1.3, space_after=4)
    rect(s, ML + 0.4, y + 4.32, CW - 0.8, 0.012, fill="line")
    txt(s, ML + 0.4, y + 4.44, CW - 0.8, 0.3,
        "초등학교 과제의 허용 범위는 담임 선생님의 안내가 우선입니다.",
        size=13.5, bold=True, color="teal")
    footer(s, 18, SRC_MOE, link=URL_MOE)
    notes(s, "학부모가 가장 궁금해하는 지점입니다. 핵심은 ‘무조건 안 된다’가 아니라 ‘교사가 정한 범위 안에서’입니다.\n"
             "안내 시 주의: 이 방안은 수행평가 관리에 초점이 있고 중·고등학교 상황이 중심입니다. "
             "초등학교 과제에 그대로 적용되는 규정이 아니라 방향을 보여 주는 자료로 소개해 주십시오. "
             "우리 학교·우리 학년의 실제 기준은 12장의 체크리스트로 확인하는 것이 정확합니다.\n"
             "표기 지도(②) 내용도 함께 언급하면 좋습니다. 자료 탐색 등에 AI를 활용한 경우 "
             "사용한 AI의 종류, 입력한 질문(프롬프트), 결과물에 반영한 방식과 부분, 출처를 적도록 안내합니다. "
             "즉 ‘쓰면 안 된다’가 아니라 ‘쓴 것을 밝힌다’가 원칙입니다.")
    return s


def s18(prs):
    s = blank(prs)
    y = title(s, "어디까지가 도움일까요?", kicker="지원 수준 4단계",
              sub="같은 AI라도 무엇을 요청하느냐에 따라 단계가 달라집니다.")
    steps = [("개념 설명", "“분수가 뭔지\n쉽게 설명해 줘”", "green", "greenbg"),
             ("한 단계 힌트", "“정답 말고\n첫 번째 힌트만”", "green", "greenbg"),
             ("피드백", "“내가 쓴 글에서\n어색한 곳 찾아 줘”", "amber", "amberbg"),
             ("작성 대행", "“독후감을\n대신 써 줘”", "red", "redbg")]
    cw = 2.55
    gap = (CW - 4 * cw) / 3
    for i, (h, ex, col, bg) in enumerate(steps):
        x = ML + i * (cw + gap)
        rrect(s, x, y + 0.45, cw, 2.2, fill=bg, line=None, radius=0.1)
        numbadge(s, x + 0.28, y + 0.7, 0.4, i + 1, fill=col, size=14)
        txt(s, x + 0.28, y + 1.25, cw - 0.56, 0.4, h, size=17.5, bold=True, color=col)
        txt(s, x + 0.28, y + 1.75, cw - 0.56, 0.7, ex.split("\n"), size=13, color="body", spacing=1.3)
        if i < 3:
            arrow(s, x + cw + gap / 2 - 0.16, y + 1.4, 0.32, 0.26, fill="line")
    rect(s, ML, y + 2.92, CW, 0.05, fill="line")
    txt(s, ML, y + 3.05, 4.0, 0.3, "◀ 아이가 생각합니다", size=13, bold=True, color="green")
    txt(s, ML + CW - 4.0, y + 3.05, 4.0, 0.3, "AI가 대신합니다 ▶", size=13, bold=True,
        color="red", align=PP_ALIGN.RIGHT)
    rrect(s, ML, y + 3.55, CW, 0.9, fill="tintteal", line=None, radius=0.12)
    rich(s, ML + 0.4, y + 3.75, CW - 0.8, 0.55,
         [[("선은 과제마다 다릅니다. ", "body", False),
           ("“이 과제로 재려던 능력을 AI가 대신하고 있나?”", "teal", True),
           (" 이것만 따져 보시면 됩니다.", "body", False)]], size=14.5)
    footer(s, 19, SRC_PNAS, link=URL_PNAS)
    notes(s, "8장의 연구와 직접 연결됩니다. 정답을 그대로 주는 방식(4단계 쪽)이 학습을 해쳤고, "
             "힌트를 주도록 설계한 방식(2단계 쪽)은 그렇지 않았습니다.\n"
             "중요한 단서: 글쓰기 과제에서 ‘맞춤법 검사’는 초록이지만, 평가 목표가 ‘맞춤법’이라면 같은 행동이 빨강이 됩니다. "
             "그래서 단계표만으로는 부족하고 과제의 목적을 함께 봐야 합니다.\n"
             "‘아이가 설명할 수 있으면 다 괜찮다’는 말도 조심해야 합니다. 설명은 필요조건이지 충분조건이 아닙니다.")
    return s


def s19(prs):
    s = blank(prs)
    y = title(s, "세 학생 중 누가 생각하고 있나요?", kicker="퀴즈 · 손들기",
              sub="같은 독후감 과제를 세 학생이 이렇게 했습니다.")
    students = [("가 학생", "AI에게 독후감을 써 달라고 한 뒤,\n어색한 단어 몇 개만 바꿔서 냈습니다.",
                 "tint", "line"),
                ("나 학생", "직접 쓴 초고를 AI에게 보여 주고\n어디가 이해하기 어려운지 물은 뒤\n스스로 고쳤습니다.",
                 "tintblue", None),
                ("다 학생", "AI에게 줄거리를 요약하게 하고\n그 요약을 바탕으로 느낀 점만\n직접 썼습니다.",
                 "tint", "line")]
    cw, gap = 3.6, 0.42
    for i, (name, body, bg, ln) in enumerate(students):
        x = ML + i * (cw + gap)
        rrect(s, x, y + 0.3, cw, 2.5, fill=bg, line=ln, radius=0.1)
        txt(s, x + 0.32, y + 0.58, cw - 0.64, 0.4, name, size=18, bold=True,
            color="blue" if i == 1 else "ink")
        txt(s, x + 0.32, y + 1.12, cw - 0.64, 1.4, body.split("\n"), size=13.5,
            color="body", spacing=1.4)
    rrect(s, ML, y + 3.1, CW, 1.35, fill="tintteal", line=None, radius=0.1)
    rich(s, ML + 0.4, y + 3.32, CW - 0.8, 0.85,
         [[("정답은 ‘나 학생’입니다. ", "teal", True),
           ("‘가 학생’은 작성 대행이고, ‘다 학생’은 애매합니다.", "body", False)],
          [("책을 읽고 이해하는 게 과제 목표였다면, 줄거리 요약을 맡긴 순간 정작 재려던 것이 빠집니다.",
            "body", False)]],
         size=14.5, spacing=1.35, space_after=4)
    footer(s, 20)
    notes(s, "먼저 손을 들게 한 뒤 답을 공개합니다. ‘다 학생’에서 의견이 갈리는 것이 이 활동의 목적입니다.\n"
             "정답 해설: ‘다 학생’이 낸 느낀 점은 본인의 글이지만, 그 느낌의 근거가 되는 ‘읽기’를 건너뛰었습니다. "
             "과제 목표가 ‘독서’라면 빨강, 과제 목표가 ‘감상 표현’이고 책은 이미 읽은 상태라면 노랑이 됩니다.\n"
             "참가자에게 되물어 주십시오. “우리 아이 과제는 무엇을 평가하려는 것이었나요?”")
    return s


def s20(prs):
    s = blank(prs)
    y = title(s, "‘답 알려줘’를 바꿔봅시다", kicker="실습 · 프롬프트 바꾸기",
              sub="상황은 그대로 두고, 요청하는 한 줄만 바꿔 봅니다.")
    pairs = [("“이 문제 답 뭐야?”", "“정답은 말하지 말고 첫 번째 힌트만 줘.”"),
             ("“독후감 써 줘.”", "“내가 쓴 독후감에서 이해하기 어려운 문장을 찾아 줘.”"),
             ("“이거 맞아?”", "“어디서 나온 내용인지 출처를 알려 줘. 확인해 볼게.”")]
    lw = 4.5
    rw = CW - lw - 1.0
    txt(s, ML, y + 0.3, lw, 0.3, "바꾸기 전", size=13, bold=True, color="mute")
    txt(s, ML + lw + 1.0, y + 0.3, rw, 0.3, "바꾼 뒤", size=13, bold=True, color="blue")
    for i, (a, b) in enumerate(pairs):
        yy = y + 0.72 + i * 1.12
        rrect(s, ML, yy, lw, 0.88, fill="tint", line="line", radius=0.12)
        txt(s, ML + 0.28, yy + 0.27, lw - 0.56, 0.4, a, size=15, color="mute")
        arrow(s, ML + lw + 0.3, yy + 0.32, 0.42, 0.26, fill="blue")
        rrect(s, ML + lw + 1.0, yy, rw, 0.88, fill="tintblue", line=None, radius=0.12)
        txt(s, ML + lw + 1.28, yy + 0.27, rw - 0.56, 0.4, b, size=15, bold=True, color="ink")
    rrect(s, ML, y + 4.15, CW, 0.72, fill="tintteal", line=None, radius=0.12)
    txt(s, ML + 0.4, y + 4.35, CW - 0.8, 0.4,
        "옆자리 분과 하나씩 만들어 보세요. 우리 아이가 실제로 하는 질문이면 더 좋습니다.",
        size=14.5, bold=True, color="teal")
    footer(s, 21)
    notes(s, "2~3분 실습입니다. 두 명씩 짝을 지어 아이가 실제로 하는 질문 하나를 바꿔 보게 합니다.\n"
             "돌아다니며 한두 사례를 받아 전체에 공유하면 다음 장(좋은 질문의 네 요소)이 자연스럽게 이어집니다.\n"
             "요령: ‘정답은 말하지 말고’라는 한 구절만 붙여도 대부분의 AI가 힌트 방식으로 바뀝니다. "
             "이 문장을 아이에게 외우게 하는 것이 오늘 배운 것 중 가장 실용적입니다.")
    return s


def s13a(prs):
    """14장 — 초등학생이 실제로 쓸 수 있는 AI 비교표"""
    s = blank(prs)
    y = title(s, "우리 아이가 지금 쓸 수 있는 AI는?", kicker="서비스별 이용 연령",
              sub="초등학생이 직접 가입할 수 있는 범용 AI 챗봇은 사실상 없습니다.")
    # 표 머리글
    ty = y + 0.22
    cols = [0.3, 3.0, 5.5, 7.0]
    widths = [2.6, 2.4, 1.3, 4.3]
    heads = ["서비스", "가입 가능 연령", "초등학생", "조건"]
    rrect(s, ML, ty, CW, 3.68, fill="white", line="line", radius=0.06)
    rect(s, ML, ty, CW, 0.42, fill="tintteal")
    for cx, wd, hd in zip(cols, widths, heads):
        txt(s, ML + cx, ty + 0.12, wd, 0.3, hd, size=12, bold=True, color="teal",
            align=PP_ALIGN.CENTER if hd == "초등학생" else PP_ALIGN.LEFT)
    rows = [
        ("ChatGPT (OpenAI)", URL_OPENAI, "만 13세 이상", "✕", "red",
         "13~18세는 보호자 동의 필요", "g1"),
        ("Claude (Anthropic)", URL_CLAUDE, "만 18세 이상", "✕", "red",
         "보호자가 동의해도 가입 불가", "g1"),
        ("Copilot (Microsoft)", URL_COPILOT, "만 13세 이상", "✕", "red",
         "나라마다 기준이 더 높을 수 있음", "g1"),
        ("Perplexity", URL_PPLX, "만 13세 이상", "✕", "red",
         "13세 미만 이용 금지", "g1"),
        ("Gemini (Google)", URL_GEMINI, "보호자가 허용하면", "△", "amber",
         "Family Link에서 켜고 끄기", "g2"),
        ("뤼튼", URL_WRTN, "보호자 동의 시", "△", "amber",
         "가입할 때 보호자 PASS 인증", "g2"),
        ("똑똑! 수학탐험대", URL_TOCTOC, "초 1~6학년", "○", "green",
         "교육부 제공, 학교를 통해 이용", "g3"),
        ("AI펭톡", URL_PENGTALK, "초 3~6학년", "○", "green",
         "교육부·EBS 제공, 영어 말하기", "g3"),
    ]
    rh = 0.4
    for i, (name, url, age, mark, col, note, grp) in enumerate(rows):
        ry = ty + 0.42 + i * rh
        if grp == "g2":
            rect(s, ML + 0.06, ry, CW - 0.12, rh, fill="tint")
        elif grp == "g3":
            rect(s, ML + 0.06, ry, CW - 0.12, rh, fill="tintteal")
        txt(s, ML + cols[0], ry + 0.1, widths[0], 0.28, name, size=12, bold=True,
            color="blue", link=url, underline=True)
        txt(s, ML + cols[1], ry + 0.1, widths[1], 0.28, age, size=12, color="body")
        txt(s, ML + cols[2], ry + 0.06, widths[2], 0.3, mark, size=15, bold=True,
            color=col, align=PP_ALIGN.CENTER)
        txt(s, ML + cols[3], ry + 0.1, widths[3], 0.28, note, size=11.5, color="mute")
    rrect(s, ML, y + 4.02, CW, 0.78, fill="tintblue", line=None, radius=0.12)
    rich(s, ML + 0.4, y + 4.22, CW - 0.8, 0.45,
         [[("지금 초등학생이 쓸 수 있는 건 대부분 ", "body", False),
           ("학교가 주는 학습 서비스", "blue", True),
           ("입니다. 나머지는 보호자 계정과 관리가 있어야 합니다.", "body", False)]],
         size=14.5)
    footer(s, 14, "각 서비스 공식 약관·고객센터 (2026년 9월 확인 기준) · 서비스 이름을 누르면 해당 안내로 이동합니다")
    notes(s, "‘그래서 뭘 쓰게 해야 하나요’라는 질문에 대한 답입니다. 표를 천천히 읽어 주세요.\n"
             "가장 중요한 메시지: 범용 AI 챗봇은 대부분 만 13세 이상입니다. 초등학생은 원칙적으로 "
             "자기 계정을 만들 수 없습니다. Claude는 보호자가 동의해도 만 18세 미만은 쓸 수 없습니다.\n"
             "예외가 두 갈래 있습니다. ①Google Gemini와 뤼튼처럼 보호자가 관리·동의하면 열리는 서비스 "
             "②똑똑! 수학탐험대, AI펭톡처럼 처음부터 초등학생을 위해 만든 학교 제공 서비스입니다. "
             "특히 후자는 교육부가 제공하는 것이라 연령·개인정보 문제에서 가장 안전합니다.\n"
             "국내법 기준도 함께 짚어 주십시오. 개인정보 보호법상 만 14세 미만 아동이 온라인 서비스에 "
             "가입할 때는 법정대리인(보호자) 동의가 필요합니다. 초등학생은 대부분 여기에 해당합니다.\n"
             "각 줄의 서비스 이름에 공식 안내 링크를 걸어 두었습니다. 발표 전에 눌러서 바뀐 내용이 없는지 "
             "확인하시면 좋겠습니다. 연령 정책은 자주 바뀝니다.\n"
             "특정 제품을 권하는 자리가 아니라는 점, 그리고 표에 없는 서비스도 많다는 점을 덧붙여 주세요.")
    return s
