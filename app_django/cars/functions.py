import numpy as np
import pandas as pd

def recommend_cars(auto_id: int, autos_encoded: pd.DataFrame, similaridades, top_n=4):
    # Obtener el índice del auto en autos_encoded
    idx = autos_encoded.index.get_loc(auto_id)
    # Obtener las similitudes del auto dado con todos los demás autos
    simil_auto = similaridades[idx]
    # Ordenar las similitudes y obtener los índices de los autos más similares
    similar_idx = np.argsort(-simil_auto)[1:top_n+1]
    # Devolver los IDs de los autos recomendados
    return autos_encoded.index[similar_idx]