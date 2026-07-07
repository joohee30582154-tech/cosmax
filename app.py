import base64
import re
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="내일 네일 - 내 주변 네일샵 찾기", layout="wide")

BASE_DIR = Path(__file__).parent
HTML_PATH = BASE_DIR / "index.html"
IMAGE_DIR = BASE_DIR / "image"
IMAGE_COUNT = 42  # index.html의 THUMB_PHOTO_COUNT 값과 동일하게 맞춰주세요


@st.cache_data(show_spinner=False)
def build_html() -> tuple[str, list[str]]:
    """index.html을 읽어서 image/nail-XX.jpg 참조를 base64 데이터로 치환한다."""
    html = HTML_PATH.read_text(encoding="utf-8")

    missing = []
    data_urls = []
    for i in range(1, IMAGE_COUNT + 1):
        img_path = IMAGE_DIR / f"nail-{i:02d}.jpg"
        if img_path.exists():
            b64 = base64.b64encode(img_path.read_bytes()).decode("utf-8")
            data_urls.append(f"data:image/jpeg;base64,{b64}")
        else:
            missing.append(img_path.name)
            data_urls.append("")  # 파일이 없으면 빈 문자열 -> onerror로 자동 숨김 처리됨

    js_array = "[" + ",".join(f'"{u}"' for u in data_urls) + "]"

    # index.html 안의 THUMB_PHOTOS 생성 코드를 base64 배열로 통째로 교체
    pattern = re.compile(r"const THUMB_PHOTOS = Array\.from\([\s\S]*?\);")
    new_html, count = pattern.subn(f"const THUMB_PHOTOS = {js_array};", html)

    if count == 0:
        st.warning(
            "⚠️ index.html에서 THUMB_PHOTOS 코드를 찾지 못했습니다. "
            "index.html 원본이 수정되었다면 app.py의 치환 로직도 함께 확인해주세요."
        )
        new_html = html

    return new_html, missing


html_content, missing_images = build_html()

if missing_images:
    st.info(
        f"이미지 {len(missing_images)}개를 찾지 못했습니다 (예: {missing_images[0]}). "
        "`image/` 폴더에 nail-01.jpg ~ nail-27.jpg 형식으로 파일을 넣어주세요. "
        "해당 카드의 썸네일은 배경 그라데이션만 표시됩니다."
    )

components.html(html_content, height=900, scrolling=True)
