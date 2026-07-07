import cv2
import numpy as np
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel
import base64
import json
import uuid
import os

from backend.utils.quality import ImageQualityAssessor
from backend.services.predict import Predictor
from backend.utils.clinical import generate_clinical_findings, generate_recommendations
from backend.services.reports import ReportGenerator
from backend.services.gradcam import GradCAM

# Initialize components
router = APIRouter()
assessor = ImageQualityAssessor()
predictor = Predictor() # Add model_path="checkpoints/best_model.pth" when trained
report_gen = ReportGenerator()

# In-memory storage for testing (use a real DB/Redis in prod)
session_store = {}

@router.get("/health")
async def health_check():
    return {"status": "healthy", "version": "EN-B3-DR-v1.0"}

@router.post("/upload")
async def upload_image(image: UploadFile = File(...)):
    """
    Handles image upload, converts to OpenCV format, and stores in session.
    """
    try:
        contents = await image.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.BGR2RGB)
        
        session_id = str(uuid.uuid4())
        session_store[session_id] = {"original_image": img}
        
        return {"session_id": session_id, "message": "Image uploaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/image-quality")
async def check_quality(session_id: str = Form(...)):
    if session_id not in session_store:
        raise HTTPException(status_code=404, detail="Session not found.")
        
    img = session_store[session_id]["original_image"]
    is_pass, reason, details = assessor.assess_quality(img)
    
    return {
        "is_pass": is_pass,
        "reason": reason,
        "details": details
    }

@router.post("/predict")
async def run_prediction(session_id: str = Form(...)):
    if session_id not in session_store:
        raise HTTPException(status_code=404, detail="Session not found.")
        
    img = session_store[session_id]["original_image"]
    
    # Run prediction
    try:
        results = predictor.predict(img)
        session_store[session_id]["prediction"] = results
        
        # Generate findings and recommendations based on grade
        grade = results["grade"]
        findings = generate_clinical_findings(grade)
        recommendations = generate_recommendations(grade)
        
        session_store[session_id]["findings"] = findings
        session_store[session_id]["recommendations"] = recommendations
        
        results["findings"] = findings
        results["recommendations"] = recommendations
        
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@router.post("/gradcam")
async def generate_gradcam(session_id: str = Form(...)):
    if session_id not in session_store:
        raise HTTPException(status_code=404, detail="Session not found.")
        
    img = session_store[session_id]["original_image"]
    
    try:
        # Initialize GradCAM with the specific conv layer of efficientnet
        # In timm's efficientnet, it's usually conv_head
        target_layer = predictor.model.conv_head
        cam = GradCAM(predictor.model, target_layer)
        
        # Prepare image (same as predict)
        augmented = predictor.transforms(image=img)
        input_tensor = augmented['image'].unsqueeze(0).to(predictor.device)
        
        heatmap = cam.generate_heatmap(input_tensor)
        overlay = cam.overlay_heatmap(img, heatmap)
        
        session_store[session_id]["gradcam_image"] = overlay
        
        # Convert to base64 for frontend
        _, buffer = cv2.imencode('.jpg', cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR))
        b64_str = base64.b64encode(buffer).decode('utf-8')
        
        return {"gradcam_base64": f"data:image/jpeg;base64,{b64_str}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Grad-CAM generation failed: {str(e)}")

@router.post("/generate-report")
async def generate_pdf_report(
    session_id: str = Form(...),
    patient_data: str = Form(...) # JSON string
):
    if session_id not in session_store:
        raise HTTPException(status_code=404, detail="Session not found.")
        
    session = session_store[session_id]
    if "prediction" not in session:
        raise HTTPException(status_code=400, detail="Prediction not run yet.")
        
    try:
        patient_dict = json.loads(patient_data)
        
        # Save temp images for reportlab
        orig_img_path = f"/tmp/{session_id}_orig.jpg"
        grad_img_path = f"/tmp/{session_id}_grad.jpg"
        
        # Make sure /tmp exists (for windows compatibility, use standard tempfile in prod)
        import tempfile
        temp_dir = tempfile.gettempdir()
        orig_img_path = os.path.join(temp_dir, f"{session_id}_orig.jpg")
        grad_img_path = os.path.join(temp_dir, f"{session_id}_grad.jpg")
        
        cv2.imwrite(orig_img_path, cv2.cvtColor(session["original_image"], cv2.COLOR_RGB2BGR))
        if "gradcam_image" in session:
            cv2.imwrite(grad_img_path, cv2.cvtColor(session["gradcam_image"], cv2.COLOR_RGB2BGR))
        else:
            grad_img_path = None
            
        pdf_buffer = report_gen.generate_pdf(
            patient_data=patient_dict,
            prediction_data=session["prediction"],
            findings=session["findings"],
            recommendations=session["recommendations"],
            image_path=orig_img_path,
            gradcam_path=grad_img_path
        )
        
        # Cleanup
        if os.path.exists(orig_img_path): os.remove(orig_img_path)
        if grad_img_path and os.path.exists(grad_img_path): os.remove(grad_img_path)
        
        return Response(content=pdf_buffer.getvalue(), media_type="application/pdf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")
