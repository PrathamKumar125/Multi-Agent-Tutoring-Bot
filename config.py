import os
from typing import Dict, Any

# Ollama configuration
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL_NAME = os.environ.get("MODEL_NAME", "qwen3:0.6b")  # Using qwen3:0.6b as default

# Physics constants for the physics agent tool
PHYSICS_CONSTANTS: Dict[str, Dict[str, Any]] = {
    "speed_of_light": {"value": 299792458, "unit": "m/s", "symbol": "c"},
    "gravitational_constant": {"value": 6.67430e-11, "unit": "m³/kg⋅s²", "symbol": "G"},
    "planck_constant": {"value": 6.62607015e-34, "unit": "J⋅s", "symbol": "h"},
    "avogadro_number": {"value": 6.02214076e23, "unit": "mol⁻¹", "symbol": "Nₐ"},
    "boltzmann_constant": {"value": 1.380649e-23, "unit": "J/K", "symbol": "k"},
    "elementary_charge": {"value": 1.602176634e-19, "unit": "C", "symbol": "e"},
    "electron_mass": {"value": 9.1093837015e-31, "unit": "kg", "symbol": "mₑ"},
    "proton_mass": {"value": 1.67262192369e-27, "unit": "kg", "symbol": "mₚ"},
}
