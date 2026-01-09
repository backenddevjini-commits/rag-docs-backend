import logging
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.document_service import save_document

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        result = save_document(file)
        # 정상 응답 통일
        return {
            "success": True,
            "data": result
        }
    
    except ValueError as e:
        # service에서 올라온 "비즈니스 에러"
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception:
        # 예상하지 못한 에러
        logger.exception("Upload failed")
        raise HTTPException(status_code=500, detail="Internal server error")