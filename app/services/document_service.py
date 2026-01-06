from pathlib import Path
import uuid
from fastapi import UploadFile

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

def save_document(file: UploadFile) -> dict:
    """
    업로드된 파일을 서버에 저장하고
    저장 정보(id, filename, saved_as)를 반환한다.
    """
    
    if not file.filename:
        raise ValueError("No filename")
    
    file_id = str(uuid.uuid4())
    file_ext = Path(file.filename).suffix
    save_path = UPLOAD_DIR / f"{file_id}{file_ext}"

    contents = file.file.read()
    save_path.write_bytes(contents)

    return {
        "id": file_id,
        "filename": file.filename,
        "saved_as": save_path.name
    }