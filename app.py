import json
import re
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

# ----------------------------------------------------------------------------
# 기본 설정
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="내일 네일 - 내 주변 네일샵 찾기",
    page_icon="💅",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR = Path(__file__).parent
HTML_PATH = BASE_DIR / "index.html"
STATIC_DIR = BASE_DIR / "static"

# 컴포넌트(iframe) 높이 — 필요하면 조절하세요.
APP_HEIGHT = 900


# ----------------------------------------------------------------------------
# static 폴더 안의 네일 사진 목록을 자동으로 읽어온다.
# 나중에 사진을 더 추가해도(static 폴더에 파일만 넣으면) 코드 수정 없이 반영됨.
# ----------------------------------------------------------------------------
def get_nail_images():
    if not STATIC_DIR.exists():
        return []

    exts = ("*.jpg", "*.jpeg", "*.png", "*.webp")
    files = []
    for ext in exts:
        files.extend(STATIC_DIR.glob(ext))

    def sort_key(p: Path):
        m = re.search(r"(\d+)", p.stem)
        return (int(m.group(1)) if m else 0, p.name)

    files = sorted(set(files), key=sort_key)
    return [f.name for f in files]


nail_images = get_nail_images()

if not nail_images:
    st.warning(
        "static 폴더에 네일 이미지가 없습니다. "
        "static/ 폴더에 nail-01.jpg 처럼 이미지를 넣어주세요."
    )

# ----------------------------------------------------------------------------
# index.html 로드 후, 로컬 image/nail-XX.jpg 참조 부분을
# Streamlit 정적 파일 서빙 경로(/app/static/...) + 실제 이미지 목록으로 교체
# ----------------------------------------------------------------------------
html = HTML_PATH.read_text(encoding="utf-8")

# ----------------------------------------------------------------------------
# Leaflet CDN(unpkg.com) 링크를 static 폴더에 내장된 로컬 파일로 교체.
# (Streamlit Cloud/iframe 환경에서 외부 CDN 스크립트가 CSP 등으로 차단되어
#  "L is not defined" 에러가 나는 것을 방지하기 위함)
# ----------------------------------------------------------------------------
cdn_replacements = {
    "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css": "/app/static/leaflet.css",
    "https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css": "/app/static/MarkerCluster.css",
    "https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css": "/app/static/MarkerCluster.Default.css",
    "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js": "/app/static/leaflet.js",
    "https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js": "/app/static/leaflet.markercluster.js",
}
for old_url, new_url in cdn_replacements.items():
    html = html.replace(old_url, new_url)

images_json = json.dumps(nail_images, ensure_ascii=False)

old_block = """  const THUMB_PHOTO_COUNT = 27;
  const THUMB_PHOTOS = Array.from({ length: THUMB_PHOTO_COUNT }, (_, i) =>
    `image/nail-${String(i + 1).padStart(2, '0')}.jpg`
  );"""

new_block = f"""  const THUMB_PHOTOS_LIST = {images_json};
  const THUMB_PHOTOS = THUMB_PHOTOS_LIST.map((f) => `/app/static/${{f}}`);"""

if old_block in html:
    html = html.replace(old_block, new_block)
else:
    st.error(
        "index.html의 이미지 로딩 코드를 찾지 못했습니다. "
        "index.html 파일이 변경되었는지 확인해주세요."
    )

# ----------------------------------------------------------------------------
# 렌더링
# ----------------------------------------------------------------------------
components.html(html, height=APP_HEIGHT, scrolling=False)
