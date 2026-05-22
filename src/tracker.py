import json
import os
import numpy as np
from datetime import datetime

class _NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(_NumpyEncoder, self).default(obj)

def registrar_tracking(fase, fuente, reg_in, reg_out, descartados, motivo):
    # Ruta corregida
    log_path = "logs/pipeline_tracking.json"
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    
    registro = {
        "fecha": datetime.utcnow().isoformat(),
        "fase": fase, "fuente": fuente,
        "entrada": reg_in, "salida": reg_out,
        "descartados": descartados, "motivo": motivo
    }
    
    datos = []
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            datos = json.load(f)
            
    datos.append(registro)
    with open(log_path, "w") as f:
        json.dump(datos, f, indent=4, cls=_NumpyEncoder)
