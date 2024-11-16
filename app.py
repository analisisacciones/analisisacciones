import yfinance as yf
import streamlit as st

# Función para corregir datos
def corregir_datos(valor):
    if valor == "N/A":
        return valor
    if valor > 200:  # Solo dividir si el valor es mayor a 200
        return round(valor / 100, 2)
    return round(valor, 2)

# Funciones de cálculo
def calcular_pe_trailing(pe_trailing):
    if pe_trailing == "N/A":
        return 0
    elif pe_trailing < 16:
        return 100
    elif pe_trailing <= 22.5:
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

def calcular_pe_forward(pe_forward):
    if pe_forward == "N/A":
        return 0
    elif pe_forward < 16:
        return 100
    elif pe_forward <= 22.5:
        return 60
    else:
        return 30

# [OTRAS FUNCIONES DE CÁLCULO OMITIDAS POR BREVEDAD...]
# Incluye todas las funciones de cálculo de tu código anterior.

# Función para obtener los datos
def obtener_datos(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        data = ticker.info

        pe_trailing = data.get('trailingPE', 'N/A')
        pe_forward = data.get('forwardPE', 'N/A')

        # Aplicar corrección a P/E y P/E forward
        if pe_trailing != 'N/A':
            pe_trailing = corregir_datos(pe_trailing)

        if pe_forward != 'N/A':
            pe_forward = corregir_datos(pe_forward)

        return {
            'nombre': data.get('shortName', 'N/A'),
            'pe_trailing': pe_trailing,
            'pe_forward': pe_forward,
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
    puntuacion = sum(p * v / 100 for p, v in zip(pesos, valores))
    return round(puntuacion / 10, 2)

# Streamlit
def main():
    st.title("Análisis de Acciones")
    ticker_symbol = st.text_input("Introduce el símbolo de la acción:")

    if ticker_symbol:
        datos = obtener_datos(ticker_symbol)
        if "error" in datos:
            st.error(f"Error al obtener datos: {datos['error']}")
        else:
            st.subheader("Datos Financieros")
            for key, value in datos.items():
                if key != "error":
                    st.write(f"**{key.replace('_', ' ').capitalize()}:** {value}")

            st.subheader("Puntuaciones Calculadas")
            valores = [
                calcular_pe_trailing(datos['pe_trailing']),
                calcular_pe_forward(datos['pe_forward']),
                calcular_analisis_pe_forward(datos['pe_forward'], datos['pe_trailing']),
                # Añade las demás funciones de cálculo aquí...
            ]

            pesos = [8.33, 13.89, 4.17, 12.50, 9.72, 9.72, 9.72, 2.78, 1.39, 9.72, 4.17, 13.89]
            puntuacion_total = calcular_puntuacion_total(pesos, valores)

            # Mostrar puntuación con colores
            if puntuacion_total < 6:
                st.markdown(f"<p style='color:red;'>Puntuación Total (Ponderada del 1 al 10): {puntuacion_total}</p>", unsafe_allow_html=True)
            elif 6 <= puntuacion_total < 7:
                st.markdown(f"<p style='color:orange;'>Puntuación Total (Ponderada del 1 al 10): {puntuacion_total}</p>", unsafe_allow_html=True)
            else:
                st.markdown(f"<p style='color:green;'>Puntuación Total (Ponderada del 1 al 10): {puntuacion_total}</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
