from fastapi import APIRouter

router = APIRouter()

previsions = [
    {"heure": "18h00", "demande": 280, "production": 260, "nomination": 150, "deficit": -20},
    {"heure": "19h00", "demande": 310, "production": 265, "nomination": 150, "deficit": -45},
    {"heure": "20h00", "demande": 305, "production": 270, "nomination": 160, "deficit": -35},
    {"heure": "21h00", "demande": 290, "production": 280, "nomination": 160, "deficit": -10},
    {"heure": "22h00", "demande": 270, "production": 285, "nomination": 160, "deficit": 15},
]

@router.get("/")
def get_previsions():
    return previsions