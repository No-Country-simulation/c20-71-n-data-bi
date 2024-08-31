def transform_data(data):
    # Ejemplo: Crear una nueva columna con el retorno diario
    try:
        data['Return'] = data['Close'].pct_change()
        data = data.dropna()  # Eliminar filas con valores NaN generados por pct_change()
        return data
    except KeyError as e:
        raise KeyError(f"Columna faltante en los datos: {e}")
    except Exception as e:
        raise Exception(f"Error al transformar los datos: {e}")

# Ejemplo de uso
# transformed_data = transform_data(data)
