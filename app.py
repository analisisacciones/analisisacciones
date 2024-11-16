import yfinance as yf
import streamlit as st

# Función para limpiar y corregir los datos iniciales
def corregir_datos(datos):
    try:
        # Corrección de P/E Trailing
        if datos.get('pe_trailing', "N/A") != "N/A":
            datos['pe_trailing'] = float(datos['pe_trailing'])
            if datos['pe_trailing'] > 200:
                datos['pe_trailing'] /= 100
        else:
            datos['pe_trailing'] = "N/A"

        # Corrección de P/E Forward
        if datos.get('pe_forward', "N/A") != "N/A":
            datos['pe_forward'] = float(datos['pe_forward'])
            if datos['pe_forward'] > 200:
                datos['pe_forward'] /= 100
        else:
            datos['pe_forward'] = "N/A"

        # Corrección de diferencia de precios
        if datos.get('precio_actual', "N/A") != "N/A" and datos.get('precio_esperado', "N/A") != "N/A":
            datos['precio_actual'] = float(datos['precio_actual'])
            datos['precio_esperado'] = float(datos['precio_esperado'])
            diferencia_absoluta = abs(datos['precio_actual'] - datos['precio_esperado'])
            max_precio = max(datos['precio_actual'], datos['precio_esperado'])
            if diferencia_absoluta > 2.5 * max_precio:
                if datos['precio_actual'] == max_precio:
                    datos['precio_actual'] /= 100
                else:
                    datos['precio_esperado'] /= 100
        else:
            datos['precio_actual'] = "N/A"
            datos['precio_esperado'] = "N/A"

    except Exception as e:
        datos["error_correccion"] = str(e)

    return datos

# Función para obtener los datos de yfinance
def obtener_datos(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        data = ticker.info
        datos = {
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
        return corregir_datos(datos)  # Corrige los datos antes de retornarlos
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
