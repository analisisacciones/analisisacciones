import yfinance as yf
import streamlit as st

# Función para formatear números grandes
def formatear_numero(numero):
    if numero == "N/A" or numero is None:
        return "N/A"
    if abs(numero) >= 1e9:  # Billones
        return f"{round(numero / 1e9, 2)}B"
    elif abs(numero) >= 1e6:  # Millones
        return f"{round(numero / 1e6, 2)}M"
    else:
        return f"{round(numero, 2)}"

# Función para formatear porcentajes
def formatear_porcentaje(valor):
    if valor == "N/A" or valor is None:
        return "N/A"
    return f"{round(valor * 100, 2)}%"

# Función para corregir datos
def corregir_datos(valor):
    if valor == "N/A":
        return valor
    if valor > 200:  # Solo dividir si el valor es mayor a 200
        return round(valor / 100, 2)
    return round(valor, 2)

# Función para corregir precio actual y esperado si la diferencia es mayor al 250%
def corregir_precios(precio_actual, precio_esperado):
    if precio_actual == "N/A" or precio_esperado == "N/A":
        return precio_actual, precio_esperado
    diferencia = abs(precio_esperado - precio_actual) / min(precio_actual, precio_esperado)
    if diferencia > 2.5:  # Más del 250%
        if precio_actual > precio_esperado:
            precio_actual = round(precio_actual / 100, 2)
        else:
            precio_esperado = round(precio_esperado / 100, 2)
    return precio_actual, precio_esperado

# Función para obtener los datos
def obtener_datos(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        data = ticker.info

        pe_trailing = data.get('trailingPE', 'N/A')
        pe_forward = data.get('forwardPE', 'N/A')
        precio_actual = data.get('currentPrice', 'N/A')
        precio_esperado = data.get('targetMeanPrice', 'N/A')

        # Aplicar corrección a P/E y P/E forward
        if pe_trailing != 'N/A':
            pe_trailing = corregir_datos(pe_trailing)

        if pe_forward != 'N/A':
            pe_forward = corregir_datos(pe_forward)

        # Aplicar corrección a precios si hay más del 250% de diferencia
        precio_actual, precio_esperado = corregir_precios(precio_actual, precio_esperado)

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
            'precio_actual': precio_actual,
            'precio_esperado': precio_esperado
        }
    except Exception as e:
        return {"error": str(e)}

# Función de cálculo ponderado ajustado
def calcular_puntuacion_total(pesos, valores):
    if len(pesos) != len(valores):
        raise ValueError("El número de valores y pesos no coincide")
    puntuacion = sum(p * v / 100 for p, v in zip(pesos, valores))
    return round(puntuacion / 10, 2)

# Función para mostrar puntuación con colores
def mostrar_puntuacion(puntuacion_total):
    if puntuacion_total < 6:
        st.markdown(f"<h2 style='color:red;'>Puntuación de compra: {puntuacion_total}</h2>", unsafe_allow_html=True)
    elif 6 <= puntuacion_total < 7:
        st.markdown(f"<h2 style='color:orange;'>Puntuación de compra: {puntuacion_total}</h2>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h2 style='color:green;'>Puntuación de compra: {puntuacion_total}</h2>", unsafe_allow_html=True)

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

def calcular_diferencia_precio(precio_actual, precio_esperado):
    if precio_actual == "N/A" or precio_esperado == "N/A" or precio_esperado == 0:
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

# Streamlit
def main():







    



    
    st.title("Análisis de Acciones")
    ticker_symbol = st.text_input("Introduce el símbolo de la acción:")

    if ticker_symbol:
        datos = obtener_datos(ticker_symbol)
        if "error" in datos:
            st.error(f"Error al obtener datos: {datos['error']}")
        else:
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
                calcular_diferencia_precio(datos['precio_actual'], datos['precio_esperado'])
            ]

            pesos = [8.96, 4.48, 14.93, 13.43, 10.45, 10.45, 10.45, 2.99, 1.49, 4.48, 10.45, 7.46]
            puntuacion_total = calcular_puntuacion_total(pesos, valores)

            mostrar_puntuacion(puntuacion_total)

            st.subheader("Datos Financieros")
            datos_formateados = {
                "Nombre": datos["nombre"],
                "P/E Trailing": datos["pe_trailing"],
                "P/E Forward": datos["pe_forward"],
                "Margen de Beneficio": formatear_porcentaje(datos["margen_beneficio"]),
                "Relación Empresa/EBITDA": datos["relacion_ebitda"],
                "Insiders": formatear_porcentaje(datos["insiders"]),
                "Cash": formatear_numero(datos["cash"]),
                "Deuda": formatear_numero(datos["deuda"]),
                "EBITDA": formatear_numero(datos["ebitda"]),
                "Crecimiento de Ganancias": formatear_porcentaje(datos["crecimiento_ganancias"]),
                "Beta": datos["beta"],
                "Dividendos": formatear_porcentaje(datos["dividendos"]),
                "Precio Actual": datos["precio_actual"],
                "Precio Esperado": datos["precio_esperado"],
            }

            for key, value in datos_formateados.items():
                st.write(f"**{key}:** {value}")

if __name__ == "__main__":
    main()
