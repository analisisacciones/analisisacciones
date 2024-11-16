import yfinance as yf
import streamlit as st

# Funciones de cálculo con prevenciones
def calcular_pe_trailing(pe_trailing):
    try:
        pe_trailing = float(pe_trailing)
    except (ValueError, TypeError):
        return 0
    
    if pe_trailing > 200:
        pe_trailing /= 100  # Prevención para P/E Trailing > 200
    if pe_trailing < 16:
        return 100
    elif pe_trailing <= 22.5:
        return 60
    else:
        return 30

def calcular_analisis_pe_forward(pe_forward, pe_trailing):
    try:
        pe_forward = float(pe_forward)
        pe_trailing = float(pe_trailing)
    except (ValueError, TypeError):
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
    try:
        pe_forward = float(pe_forward)
    except (ValueError, TypeError):
        return 0

    if pe_forward > 200:
        pe_forward /= 100
    elif pe_forward < 16:
        return 100
    elif pe_forward <= 22.5:
        return 60
    else:
        return 30

def calcular_margen_beneficio(margen_beneficio):
    try:
        margen_beneficio = float(margen_beneficio)
    except (ValueError, TypeError):
        return 0

    if margen_beneficio <= 0.05:
        return 15
    elif margen_beneficio <= 0.1:
        return 40
    elif margen_beneficio <= 0.2:
        return 75
    else:
        return 100

def calcular_relacion_empresa_ebitda(relacion_ebitda):
    try:
        relacion_ebitda = float(relacion_ebitda)
    except (ValueError, TypeError):
        return 0

    if relacion_ebitda <= 10:
        return 100
    elif relacion_ebitda <= 15:
        return 70
    else:
        return 30

def porcentaje_insiders(valor):
    try:
        valor = float(valor)
    except (ValueError, TypeError):
        return 0

    if valor <= 0.05:
        return 15
    elif valor <= 0.1:
        return 40
    elif valor <= 0.2:
        return 75
    else:
        return 100

def calcular_crecimiento_ganancias(crecimiento_ganancias):
    try:
        crecimiento_ganancias = float(crecimiento_ganancias)
    except (ValueError, TypeError):
        return 0

    if crecimiento_ganancias <= 0.05:
        return 15
    elif crecimiento_ganancias <= 0.15:
        return 60
    elif crecimiento_ganancias <= 0.25:
        return 90
    else:
        return 100

def calcular_beta(beta):
    try:
        beta = float(beta)
    except (ValueError, TypeError):
        return 0

    if 0.8 <= beta <= 1.2:
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
    try:
        dividendos = float(dividendos)
    except (ValueError, TypeError):
        return 0

    if 0 < dividendos <= 0.02:
        return 75
    elif dividendos > 0.02:
        return 100
    else:
        return 0

def calcular_cash_deuda(cash, deuda):
    try:
        cash = float(cash)
        deuda = float(deuda)
    except (ValueError, TypeError):
        return 0

    if deuda == 0:
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
    try:
        deuda = float(deuda)
        ebitda = float(ebitda)
    except (ValueError, TypeError):
        return 0

    if ebitda == 0:
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
    try:
        precio_actual = float(precio_actual)
        precio_esperado = float(precio_esperado)
    except (ValueError, TypeError):
        return 0

    if precio_esperado > 250 * precio_actual:
        precio_esperado /= 100

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

# Función para obtener los datos
def obtener_datos(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        data = ticker.info
        return {
            'nombre': data.get('shortName', 'N/A'),
            'pe_trailing': data.get('trailingPE', 'N/A'),
            'pe_forward': data.get('forwardPE', 'N/A'),
            'margen_beneficio': data.get('profitMargins', 'N/A'),
            'relacion_ebitda': data.get('enterpriseToEbitda', 'N/A'),
            'insiders': data.get('heldPercentInsiders', 'N/A'),
            'cash': data.get('totalCash', 'N/A'),
            'deuda': data.get('totalDebt', 'N/A'),
            'ebitda': data.get('ebitda', 'N/A'),
            'crecimiento_ganancias': data.get('earningsQuarterlyGrowth', 'N/A'),
            'beta': data.get('beta', 'N/A'),
            'dividendos': data.get('dividendYield', 'N/A'),
            'precio_actual': data.get('currentPrice', 'N/A'),
            'precio_esperado': data.get('targetMeanPrice', 'N/A')
        }
    except Exception as e:
        return {"error": str(e)}

# Cálculo ponderado ajustado
def calcular_puntuacion_total(pesos, valores):
    valores = [v if isinstance(v, (int, float)) else 0 for v in valores]
    puntuacion = sum(p * v / 100 for p, v in zip(pesos, valores))
    return round(puntuacion / 10, 2)

# Streamlit
def main():
    st.title("Análisis de Acciones")
    ticker_symbol = st.text_input("Introduce el símbolo de la acción:")

    if not ticker_symbol.strip():
        st.warning("Por favor, introduce un símbolo de acción válido.")
        return

    datos = obtener_datos(ticker_symbol)
    if "error" in datos:
        st.error(f"Error al obtener datos: {datos['error']}")
        return

    st.subheader("Datos Financieros")
    for key, value in datos.items():
        if key != "error":
            st.write(f"**{key.replace('_', ' ').capitalize()}:** {value}")

    st.subheader("Puntuaciones Calculadas")

    valores = [
        calcular_pe_trailing(datos['pe_trailing']),
        calcular_pe_forward(datos['pe_forward']),
        calcular_analisis_pe_forward(datos['pe_forward'], datos['pe_trailing']),
        calcular_margen_beneficio(datos['margen_beneficio']),
        calcular_relacion_empresa_ebitda(datos['relacion_ebitda']),
        porcentaje_insiders(datos['insiders']),
        calcular_crecimiento_ganancias(datos['crecimiento_ganancias']),
        calcular_beta(datos['beta']),
        calcular_dividendos(datos['dividendos']),
        calcular_cash_deuda(datos['cash'], datos['deuda']),
        calcular_deuda_ebitda(datos['deuda'], datos['ebitda']),
        calcular_precio_esperado(datos['precio_actual'], datos['precio_esperado']),
    ]

    pesos = [8.33, 13.89, 4.17, 12.50, 9.72, 9.72, 9.72, 2.78, 1.39, 9.72, 4.17, 13.89]
    puntuacion_total = calcular_puntuacion_total(pesos, valores)
    st.write(f"**Puntuación Total:** {puntuacion_total}")

if __name__ == "__main__":
    main()
