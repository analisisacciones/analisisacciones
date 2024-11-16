import yfinance as yf
import streamlit as st

# Funciones para calcular las puntuaciones
def calcular_pe_trailing(pe_trailing):
    if pe_trailing < 16:
        return 100
    elif pe_trailing <= 22.5:
        return 60
    else:
        return 30

def calcular_analisis_pe_forward(pe_forward, pe_trailing):
    diferencia = pe_forward - pe_trailing
    if diferencia > 0:
        return 0
    elif 0 >= diferencia > -2:
        return 30
    else:
        return 100

def calcular_pe_forward(pe_forward):
    if pe_forward < 16:
        return 100
    elif pe_forward <= 22.5:
        return 60
    else:
        return 30

def calcular_margen_beneficio(margen_beneficio):
    if margen_beneficio <= 0.05:
        return 15
    elif margen_beneficio <= 0.1:
        return 40
    elif margen_beneficio <= 0.2:
        return 75
    else:
        return 100

def calcular_relacion_empresa_ebitda(relacion_ebitda):
    if relacion_ebitda <= 10:
        return 100
    elif relacion_ebitda <= 15:
        return 70
    else:
        return 30

def porcentaje_insiders(valor):
    if valor <= 0.05:
        return 15
    elif valor <= 0.1:
        return 40
    elif valor <= 0.2:
        return 75
    else:
        return 100

def calcular_crecimiento_ganancias(crecimiento_ganancias):
    if crecimiento_ganancias <= 0.05:
        return 15
    elif crecimiento_ganancias <= 0.15:
        return 60
    elif crecimiento_ganancias <= 0.25:
        return 90
    else:
        return 100

def calcular_beta(beta):
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
    if dividendos == "N/A":
        return 0
    elif 0 < dividendos <= 0.02:
        return 75
    elif dividendos > 0.02:
        return 100
    else:
        return 0

def calcular_cash_deuda(cash, deuda):
    if deuda == 0:  # Evitar división por cero
        return None
    
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
        return None  # Valor no válido

def calcular_deuda_ebitda(deuda, ebitda):
    if ebitda == 0:  # Evitar división por cero
        return None
    
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
        return None  # Valor no válido

def calcular_precio_esperado(precio_actual, precio_esperado):
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


# Función para obtener los datos de Yahoo Finance
def obtener_datos(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.info

    datos = {
        'nombre': data.get('shortName', 'N/A'),
        'symbol': data.get('symbol', 'N/A'),
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

    return datos


# Interfaz en Streamlit
def main():
    st.title("Análisis de Acciones")
    ticker_symbol = st.text_input("Introduce el símbolo de la acción (por ejemplo, TSLA para Tesla):")

    if ticker_symbol:
        try:
            # Obtener los datos
            datos = obtener_datos(ticker_symbol)

            # Mostrar los datos originales de Yahoo Finance
            st.subheader("Datos Financieros:")
            for key, value in datos.items():
                st.write(f"{key}: {value}")

            # Calcular las puntuaciones
            st.subheader("Puntuaciones Calculadas:")
            st.write(f"P/E Trailing: {calcular_pe_trailing(datos['pe_trailing'])}")
            st.write(f"Análisis P/E Forward: {calcular_analisis_pe_forward(datos['pe_forward'], datos['pe_trailing'])}")
            st.write(f"P/E Forward: {calcular_pe_forward(datos['pe_forward'])}")
            st.write(f"Margen de Beneficio: {calcular_margen_beneficio(datos['margen_beneficio'])}")
            st.write(f"Relación Empresa/EBITDA: {calcular_relacion_empresa_ebitda(datos['relacion_ebitda'])}")
            st.write(f"Porcentaje de Insiders: {porcentaje_insiders(datos['insiders'])}")
            st.write(f"Crecimiento de Ganancias: {calcular_crecimiento_ganancias(datos['crecimiento_ganancias'])}")
            st.write(f"Beta: {calcular_beta(datos['beta'])}")
            st.write(f"Dividendos: {calcular_dividendos(datos['dividendos'])}")
            st.write(f"Cash/Deuda: {calcular_cash_deuda(datos['cash'], datos['deuda'])}")
            st.write(f"Deuda/EBITDA: {calcular_deuda_ebitda(datos['deuda'], datos['ebitda'])}")
            st.write(f"Precio Esperado: {calcular_precio_esperado(datos['precio_actual'], datos['precio_esperado'])}")

        except Exception as e:
            st.error(f"Error al obtener los datos: {e}")

if __name__ == "__main__":
    main()
