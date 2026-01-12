from typing import List

def chunk_text(
        text: str,
        chunk_size: int = 500,
        overlap: int = 50
) -> List[str]:
    """
    긴 텍스트를 일정 길이의 chunk로 분할한다.

    - chunk_size : 한 chunk의 최대 길이
    - overlap : 이전 chunk와 겹치는 문자 수
    """

    if not text:
        return []
    
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        # 다음 chunk 시작 위치 (overlap 적용)
        start = end - overlap

        if start < 0:
            start = 0

    return chunks

if __name__ == "__main__":
    sample = "A" * 1200
    chunks = chunk_text(sample)

    print(f"총 chunk 수: {len(chunks)}")
    for i, c in enumerate(chunks):
        print(f"{i+1}: {len(c)} chars")