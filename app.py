# Funciones de cálculo
def calcular_pe_trailing(pe_trailing):
    if pe_trailing == "N/A":
        return 0
    elif pe_trailing > 200:
        pe_trailing /= 100  # Prevención para P/E Trailing > 200
    if pe_trailing < 16:
        return 100
    elif pe_trailing <= 22.5:
        return 60
    else:
        return 30

def calcular_analisis_pe_forward(pe_forward, pe_trailing):
    if pe_forward == "N/A" or pe_trailing == "N/A":
        return 0
    if pe_forward > 200:
        pe_forward /= 100  # Prevención para P/E Forward > 200
    diferencia = pe_forward - pe_trailing
    if diferencia > 0:
        return 0
    elif 0 >= diferencia > -2:
        return 30
    else:
        return 100

def calcular_pe_forward(pe_forward):
    if pe_forward == "N/A":
        return 0
    if pe_forward > 200:
        pe_forward /= 100  # Prevención para P/E Forward > 200
    elif pe_forward < 16:
        return 100
    elif pe_forward <= 22.5:
        return 60
    else:
        return 30

def calcular_margen_beneficio(margen_beneficio):
    if margen_beneficio == "N/A":
        return 0
    elif margen_beneficio <= 0.05:
        return 15
    elif margen_beneficio <= 0.1:
        return 40
    elif margen_beneficio <= 0.2:
        return 75
    else:
        return 100

def calcular_relacion_empresa_ebitda(relacion_ebitda):
    if relacion_ebitda == "N/A":
        return 0
    elif relacion_ebitda <= 10:
        return 100
    elif relacion_ebitda <= 15:
        return 70
    else:
        return 30

def porcentaje_insiders(valor):
    if valor == "N/A":
        return 0
    elif valor <= 0.05:
        return 15
    elif valor <= 0.1:
        return 40
    elif valor <= 0.2:
        return 75
    else:
        return 100

def calcular_crecimiento_ganancias(crecimiento_ganancias):
    if crecimiento_ganancias == "N/A":
        return 0
    elif crecimiento_ganancias <= 0.05:
        return 15
    elif crecimiento_ganancias <= 0.15:
        return 60
    elif crecimiento_ganancias <= 0.25:
        return 90
    else:
        return 100

def calcular_beta(beta):
    if beta == "N/A":
        return 0
    elif 0.8 <= beta <= 1.2:
        return 100
    elif 0 < beta <= 0.3:
        return 20
    elif 0.3 < beta < 0.8:
        return 70
    elif 1.2 <= beta < 1.6:
        return 60
    elif 1.6 <= beta < 2:
        return 40
    elif beta > 2:
        return 20
    else:
        return 0

def calcular_dividendos(dividendos):
    if dividendos == "N/A":
        return 0
    elif 0 < dividendos <= 0.02:
        return 75
    elif dividendos > 0.02:
        return 100
    else:
        return 0

def calcular_cash_deuda(cash, deuda):
    if cash == "N/A" or deuda == "N/A" or deuda == 0:
        return 0
    ratio = (cash - deuda) / deuda
    if 0 <= ratio <= 1:
        return 80
    elif ratio > 1:
        return 100
    elif -0.5 < ratio < 0:
        return 50
    elif ratio < -0.5:
        return 10
    else:
        return 0

def calcular_deuda_ebitda(deuda, ebitda):
    if deuda == "N/A" or ebitda == "N/A" or ebitda == 0:
        return 0
    ratio = deuda / ebitda
    if 0 <= ratio <= 2.5:
        return 100
    elif 2.5 < ratio <= 4:
        return 60
    elif 4 < ratio <= 10:
        return 10
    elif ratio > 10:
        return 0
    else:
        return 0

def calcular_precio_esperado(precio_actual, precio_esperado):
    if precio_actual == "N/A" or precio_esperado == "N/A":
        return 0
    diferencia = (precio_esperado - precio_actual) / precio_actual
    if diferencia < 0:
        return 0
    elif 0 <= diferencia < 0.1:
        return 30
    elif 0.1 <= diferencia < 0.2:
        return 60
    elif 0.2 <= diferencia < 0.4:
        return 80
    else:
        return 100

# Cálculo ponderado ajustado
def calcular_puntuacion_total(pesos, valores):
    puntuacion = sum(p * v / 100 for p, v in zip(pesos, valores))
    return round(puntuacion / 10, 2)

# Streamlit
def main():
    st.title("Análisis de Acciones")
    ticker_symbol = st.text_input("Introduce el símbolo de la acción:")
