"""Resume upload endpoint — Milestone 3."""
from __future__ import annotations

from fastapi import APIRouter, File, UploadFile

from app.schemas.resume import ResumeUploadResponse
from app.services.document_processor import DocumentProcessor

router = APIRouter()
_processor = DocumentProcessor()


@router.post(
    "/upload",
    response_model=ResumeUploadResponse,
    summary="Upload Resume",
    description=(
        "Upload a resume file (PDF, DOCX, or TXT). "
        "The file is validated for type and size, text is extracted in-memory, "
        "and the file is NOT stored permanently."
    ),
)
async def upload_resume(
    file: UploadFile = File(..., description="Resume file (PDF, DOCX, TXT; max 10MB)"),
) -> ResumeUploadResponse:
    """Validate and extract text from an uploaded resume file.

    Args:
        file: The uploaded resume file.

    Returns:
        ResumeUploadResponse with extracted text and metadata.

    Raises:
        UnsupportedFileTypeError: If the file type is not supported.
        FileTooLargeError: If the file exceeds the size limit.
        DocumentProcessingError: If extraction fails.
        EmptyDocumentError: If the document has no extractable text.
    """
    content = await file.read()
    result = _processor.validate_and_extract(
        file_content=content,
        filename=file.filename or "resume",
        declared_content_type=file.content_type or "application/octet-stream",
    )
    return ResumeUploadResponse(**result)
