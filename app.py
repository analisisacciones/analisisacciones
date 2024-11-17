import yfinance as yf
import streamlit as st

# Funciones para calcular valores intermedios según las métricas
def calcular_pe_trailing(pe_trailing):
    if pe_trailing == "N/A":
        return 0
    elif pe_trailing < 16:
        return 100
    elif pe_trailing <= 22.5:
        return 60
    else:
        return 30

def calcular_pe_forward(pe_forward):
    if pe_forward == "N/A":
        return 0
    elif pe_forward < 16:
        return 100
    elif pe_forward <= 22.5:
        return 60
    else:
        return 30

def calcular_analisis_pe_forward(pe_forward, pe_trailing):
    if pe_forward == "N/A" or pe_trailing == "N/A":
        return 0
    diferencia = pe_forward - pe_trailing
    if diferencia > 0:
        return 0
    elif 0 >= diferencia > -2:
        return 30
    else:
        return 100

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
    variacion = (precio_esperado - precio_actual) / precio_actual
    if variacion < 0:
        return 0
    elif 0 <= variacion < 0.1:
        return 30
    elif 0.1 <= variacion < 0.2:
        return 60
    elif 0.2 <= variacion < 0.4:
        return 80
    else:
        return 100

# Función para calcular la puntuación total con redondeos intermedios
def calcular_puntuacion_total(pesos, valores):
    resultados_parciales = [round(p * v / 100, 2) for p, v in zip(pesos, valores)]  # Redondeo intermedio
    suma_ponderada = sum(resultados_parciales)
    return round(suma_ponderada / 10, 2)

# Función para obtener datos de yfinance
def obtener_datos(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.info
    return {
        "P/E Trailing": data.get("trailingPE", "N/A"),
        "P/E Forward": data.get("forwardPE", "N/A"),
        "Margen de Beneficio": data.get("profitMargins", "N/A"),
        "Relación Empresa/EBITDA": data.get("enterpriseToEbitda", "N/A"),
        "Insiders": data.get("heldPercentInsiders", "N/A"),
        "Cash": data.get("totalCash", "N/A"),
        "Deuda": data.get("totalDebt", "N/A"),
        "EBITDA": data.get("ebitda", "N/A"),
        "Crecimiento de Ganancias": data.get("earningsQuarterlyGrowth", "N/A"),
        "Beta": data.get("beta", "N/A"),
        "Dividendos": data.get("dividendYield", "N/A"),
        "Precio Actual": data.get("currentPrice", "N/A"),
        "Precio Esperado": data.get("targetMeanPrice", "N/A"),
    }

# Streamlit - Interfaz principal
def main():
    st.title("Análisis de Acciones")
    ticker_symbol = st.text_input("Introduce el símbolo de la acción:")
    if ticker_symbol:
        datos = obtener_datos(ticker_symbol)

        # Calcular valores
        valores = [
            calcular_pe_trailing(datos["P/E Trailing"]),
            calcular_pe_forward(datos["P/E Forward"]),
            calcular_analisis_pe_forward(datos["P/E Forward"], datos["P/E Trailing"]),
            calcular_margen_beneficio(datos["Margen de Beneficio"]),
            calcular_relacion_empresa_ebitda(datos["Relación Empresa/EBITDA"]),
            porcentaje_insiders(datos["Insiders"]),
            calcular_crecimiento_ganancias(datos["Crecimiento de Ganancias"]),
            calcular_beta(datos["Beta"]),
            calcular_dividendos(datos["Dividendos"]),
            calcular_cash_deuda(datos["Cash"], datos["Deuda"]),
            calcular_deuda_ebitda(datos["Deuda"], datos["EBITDA"]),
            calcular_precio_esperado(datos["Precio Actual"], datos["Precio Esperado"]),
        ]

        # Pesos
        pesos = [8.96, 14.93, 4.48, 13.43, 10.45, 10.45, 10.45, 2.99, 1.49, 4.48, 10.45, 7.46]

        # Puntuación Final
        puntuacion_final = calcular_puntuacion_total(pesos, valores)

        # Mostrar resultados
        st.write(f"**Puntuación Final:** {puntuacion_final}")
        st.subheader("Datos Financieros:")
        for key, value in datos.items():
            st.write(f"**{key}:** {value}")

if __name__ == "__main__":
    main()
