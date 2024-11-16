# Streamlit
def main():
    st.title("Análisis de Acciones")
    ticker_symbol = st.text_input("Introduce el símbolo de la acción:")

    if ticker_symbol:
        datos = obtener_datos(ticker_symbol)
        if "error" in datos:
            st.error(f"Error al obtener datos: {datos['error']}")
        else:
            st.subheader("Datos Obtenidos")
            for clave, valor in datos.items():
                st.write(f"{clave}: {valor}")

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

            # Mostrar valores calculados junto con los indicadores originales
            indicadores = [
                "P/E Trailing", "P/E Forward", "Análisis P/E Forward", "Margen de Beneficio",
                "Relación Empresa/EBITDA", "Porcentaje Insiders", "Crecimiento de Ganancias",
                "Beta", "Dividendos", "Cash/Deuda", "Deuda/EBITDA", "Precio Esperado"
            ]
            
            for indicador, valor, puntuacion in zip(indicadores, datos.values(), valores):
                st.write(f"{indicador}: {valor} → Puntuación: {puntuacion}")
            
            # Mostrar puntuación total
            st.subheader("Puntuación Total")
            st.write(f"Puntuación Total (Ponderada del 1 al 10): {puntuacion_total}")

if __name__ == "__main__":
    main()
