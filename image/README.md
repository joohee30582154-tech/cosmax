# 이미지 폴더 안내

이 폴더에 네일아트 썸네일 이미지를 넣어주세요.

- 파일명: `nail-01.jpg`, `nail-02.jpg`, ... `nail-42.jpg` (2자리 숫자, 총 42장)
- 형식: jpg 권장 (다른 확장자를 쓰려면 app.py의 `nail-{i:02d}.jpg` 부분과
  `data:image/jpeg;base64,` 부분을 함께 수정해야 합니다)
- 일부만 있어도 됩니다. 없는 번호는 자동으로 빈 배경(그라데이션)만 표시됩니다.

GitHub 저장소 구조 예시:

```
your-repo/
├── app.py
├── requirements.txt
├── index.html
└── image/
    ├── nail-01.jpg
    ├── nail-02.jpg
    ...
    └── nail-27.jpg
```
