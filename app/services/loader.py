# services/loader.py
from pathlib import Path
import pdfplumber

def extract_text(file_path: Path) -> str:
    """
    PDF 또는 TXT 파일에서 텍스트를 추출
    """
    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} 가 존재하지 않습니다.")

    if file_path.suffix.lower() == ".pdf":
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    # 불필요한 줄바꿈 제거, 문장 단위로 연결
                    cleaned = " ".join(line.strip() for line in page_text.splitlines())
                    text += cleaned + "\n"
        return text

    elif file_path.suffix.lower() == ".txt":
        return file_path.read_text(encoding="utf-8")

    else:
        raise ValueError("지원하지 않는 파일 형식입니다.")

# ===============================
# 단독 실행 테스트용
# ===============================
if __name__ == "__main__":
    # 테스트용 PDF/TXT 경로
    test_files = ["uploads/sample.pdf", "uploads/sample.txt"]

    for file in test_files:
        path = Path(file)
        try:
            text = extract_text(path)
            print(f"\n=== {file} 내용 미리보기 (앞 500자) ===")
            print(text[:500])
        except Exception as e:
            print(f"Error: {e}")
