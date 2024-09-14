#el modelo de tabla para cada empresa energética

CREATE TABLE IF NOT EXISTS {table_name} (
            "Date" DATE,
            "Open" FLOAT,
            "High" FLOAT,
            "Low" FLOAT,
            "Close" FLOAT,
            "Volume" BIGINT,
            "Dividends" FLOAT,
            "Stock_Splits" FLOAT
        );