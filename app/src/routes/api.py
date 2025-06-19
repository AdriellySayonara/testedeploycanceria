from fastapi import APIRouter
from src.endpoints import auth, patients, images, exams, classifiers

router = APIRouter()
router.include_router(auth.router)
router.include_router(classifiers.router)
router.include_router(patients.router)
router.include_router(images.router)
router.include_router(exams.router)