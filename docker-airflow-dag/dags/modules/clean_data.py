def clean_dataset(data):
    try:
        # Ejemplo: Eliminar duplicados y manejar valores faltantes
        data = data.drop_duplicates()
        data = data.fillna(method='ffill')  # Rellenar valores faltantes con el último valor válido
        return data
    except Exception as e:
        raise Exception(f"Error al limpiar los datos: {e}")

# Ejemplo de uso
# cleaned_data = clean_dataset(transformed_data)
