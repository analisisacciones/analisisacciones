import yfinance as yf
import streamlit as st

# Función para obtener y dar formato a los datos financieros
def obtener_datos(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.info

    # Extrae y formatea los datos como en el código que compartiste
    output = [
        f"**Nombre corto**: {data.get('shortName', 'N/A')}",
        f"**Símbolo**: {data.get('symbol', 'N/A')}",
        f"**P/E trailing**: {data.get('trailingPE', 'N/A'):.2f}".replace('.', ',') if data.get('trailingPE') else "N/A",
        f"**P/E forward**: {data.get('forwardPE', 'N/A'):.2f}".replace('.', ',') if data.get('forwardPE') else "N/A",
        f"**Margen de beneficio**: {data.get('profitMargins', 'N/A'):.2%}".replace('.', ',') if data.get('profitMargins') else "N/A",
        f"**Enterprise to EBITDA**: {data.get('enterpriseToEbitda', 'N/A'):.2f}".replace('.', ',') if data.get('enterpriseToEbitda') else "N/A",
        f"**Porcentaje de insiders**: {data.get('heldPercentInsiders', 'N/A'):.2%}".replace('.', ',') if data.get('heldPercentInsiders') else "N/A",
        f"**Efectivo total**: {data.get('totalCash', 'N/A'):.2f}".replace('.', ',') if data.get('totalCash') else "N/A",
        f"**Deuda total**: {data.get('totalDebt', 'N/A'):.2f}".replace('.', ',') if data.get('totalDebt') else "N/A",
        f"**EBITDA**: {data.get('ebitda', 'N/A'):.2f}".replace('.', ',') if data.get('ebitda') else "N/A",
        f"**Crecimiento trimestral de ganancias**: {data.get('earningsQuarterlyGrowth', 'N/A'):.2f}".replace('.', ',') if data.get('earningsQuarterlyGrowth') else "N/A",
        f"**Beta**: {data.get('beta', 'N/A'):.2f}".replace('.', ',') if data.get('beta') else "N/A",
        f"**Rendimiento del dividendo**: {data.get('dividendYield', 'N/A'):.2%}".replace('.', ',') if data.get('dividendYield') else "N/A",
        f"**Precio actual**: {data.get('currentPrice', 'N/A'):.2f}".replace('.', ',') if data.get('currentPrice') else "N/A",
        f"**Precio objetivo promedio**: {data.get('targetMeanPrice', 'N/A'):.2f}".replace('.', ',') if data.get('targetMeanPrice') else "N/A",
        f"**Fecha de actualización**: {ticker.history(period='1d').index[-1].strftime('%Y-%m-%d')}" if not ticker.history(period="1d").empty else "N/A"
    ]

    return output

# Interfaz en Streamlit
def main():
    st.title("Análisis de Acciones")
    ticker_symbol = st.text_input("Introduce el símbolo de la acción (por ejemplo, TSLA para Tesla):")

    if ticker_symbol:
        datos = obtener_datos(ticker_symbol)
        for linea in datos:
            st.write(linea)  # Mostrar cada línea por separado

if __name__ == "__main__":
    main()
