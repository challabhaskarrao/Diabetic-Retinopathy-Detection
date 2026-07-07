import random

def generate_clinical_findings(grade: int) -> list[str]:
    """
    Generates plausible clinical findings based on the predicted DR grade.
    0 - No DR
    1 - Mild
    2 - Moderate
    3 - Severe
    4 - Proliferative
    """
    findings = []
    
    if grade == 0:
        findings.append("No significant microvascular abnormalities detected.")
        findings.append("Macula appears unremarkable.")
        findings.append("Optic disc margins are sharp and well-defined.")
        return findings

    if grade >= 1:
        # Microaneurysms are the hallmark of Mild NPDR
        count = random.randint(1, 5) if grade == 1 else random.randint(5, 15)
        findings.append(f"Detected approximately {count} microaneurysms.")
        
    if grade >= 2:
        # Moderate NPDR
        findings.append("Dot and blot hemorrhages observed.")
        findings.append("Hard exudates present, indicating localized vascular leakage.")
        if random.random() > 0.5:
            findings.append("Cotton wool spots (soft exudates) suspected.")
            
    if grade >= 3:
        # Severe NPDR
        findings.append("Severe intraretinal microvascular abnormalities (IRMA).")
        findings.append("Venous beading is prominent in multiple quadrants.")
        findings.append("Extensive retinal hemorrhages noted.")
        
    if grade == 4:
        # PDR
        findings.append("Neovascularization at the disc (NVD) or elsewhere (NVE) detected.")
        findings.append("High risk of vitreous hemorrhage.")
        if random.random() > 0.7:
            findings.append("Signs of tractional retinal detachment suspected.")

    return findings

def generate_recommendations(grade: int) -> list[str]:
    """
    Generates standardized clinical recommendations mapped to the DR grading scale.
    """
    recs = []
    
    if grade == 0:
        recs.append("Routine annual diabetic eye screening is recommended.")
        recs.append("Maintain optimal glycemic and blood pressure control.")
    elif grade == 1:
        recs.append("Repeat screening in 6–12 months.")
        recs.append("Primary care physician should optimize glycemic and blood pressure control.")
    elif grade == 2:
        recs.append("Refer to ophthalmologist within 2-3 months for a comprehensive dilated eye exam.")
        recs.append("Consider baseline OCT to evaluate for Diabetic Macular Edema (DME).")
    elif grade == 3:
        recs.append("Urgent referral to retinal specialist within 2-4 weeks.")
        recs.append("Patient may require panretinal photocoagulation (PRP) or anti-VEGF therapy.")
    elif grade == 4:
        recs.append("Immediate retinal specialist consultation required.")
        recs.append("High risk of severe vision loss; urgent intervention (PRP/Surgery) indicated.")
        
    return recs
