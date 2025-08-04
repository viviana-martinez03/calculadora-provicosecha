import pandas as pd
import streamlit as st
import copy

# Initialize session state
if "basico" not in st.session_state:
    st.session_state.basico = 0.0
if "divisor" not in st.session_state:
    st.session_state.divisor = 220


# Function to get DataFrame data based on selected jornada
def get_jornada_data(tipo_jornada, vl_dia=0, vl_hora=0):
    """
    Returns DataFrame data based on the selected jornada type.
    Each jornada type will have different rows with HORA, DESCRIPCION, CC-NOMINA, PORCENTAJE, VALOR
    vl_dia: valor día (basico/30)
    vl_hora: valor hora (basico/divisor)
    """

    # Complete data structure - all jornadas configured with direct formulas
    jornada_data = {
        "LUNES A SABADO ORDINARIO DIURNO (06:00-18:00)": [
            {
                "HORA": "06:00 a 14:00",
                "DESCRIPCION": "Jornal",
                "CC-NOMINA": "1MF9",
                "PORCENTAJE": 100,
                "VALOR($)": vl_dia * (100 / 100),
                "HOURS_FIELD": None,  # This doesn't change with hours
                "JORNAL_FIELD": True,  # This can be multiplied
            },
            {
                "HORA": "14:00 a 18:00",
                "DESCRIPCION": "4 - Horas extras Diurnas",
                "CC-NOMINA": "M300",
                "PORCENTAJE": 125,
                "VALOR($)": vl_hora * (125 / 100) * 4,
                "HOURS_FIELD": "4",  # This can be modified
                "JORNAL_FIELD": False,
            },
        ],
        "DOMINGO DIURNO (06:00-18:00)": [
            {
                "HORA": "06:00 a 14:00",
                "DESCRIPCION": "Dominical",
                "CC-NOMINA": "1M02",
                "PORCENTAJE": 100,
                "VALOR($)": vl_dia * (100 / 100),
                "HOURS_FIELD": None,
                "JORNAL_FIELD": False,
            },
            {
                "HORA": "06:00 a 14:00",
                "DESCRIPCION": "8 - Horas diurnas dominicales",
                "CC-NOMINA": "1M06",
                "PORCENTAJE": 80,
                "VALOR($)": vl_hora * (80 / 100) * 8,
                "HOURS_FIELD": "8",
                "JORNAL_FIELD": False,
            },
            {
                "HORA": "06:00 a 14:00",
                "DESCRIPCION": "8 - Compensatorio lab.doming",
                "CC-NOMINA": "1M08",
                "PORCENTAJE": 100,
                "VALOR($)": vl_hora * (100 / 100) * 8,
                "HOURS_FIELD": "8",
                "JORNAL_FIELD": False,
            },
            {
                "HORA": "14:00 a 18:00",
                "DESCRIPCION": "4 - Hora Extra Diurna dominical (125+80)  205%",
                "CC-NOMINA": "M310",
                "PORCENTAJE": 205,
                "VALOR($)": vl_hora * (205 / 100) * 4,
                "HOURS_FIELD": "4",
                "JORNAL_FIELD": False,
            },
        ],
        "LUNES A VIERNES ORDINARIO NOCTURNO (18:00-6:00)": [
            {
                "HORA": "18:00 a 02:00",
                "DESCRIPCION": "Jornal",
                "CC-NOMINA": "1MF9",
                "PORCENTAJE": 100,
                "VALOR($)": vl_dia * (100 / 100),
                "HOURS_FIELD": None,
                "JORNAL_FIELD": True,
            },
            {
                "HORA": "21:00 a 02:00",
                "DESCRIPCION": "5 - Recargo Nocturno",
                "CC-NOMINA": "M220",
                "PORCENTAJE": 35,
                "VALOR($)": vl_hora * (35 / 100) * 5,
                "HOURS_FIELD": "5",
                "JORNAL_FIELD": False,
            },
            {
                "HORA": "02:00 a 06:00",
                "DESCRIPCION": "4 - Hora Extra Nocturna",
                "CC-NOMINA": "M305",
                "PORCENTAJE": 175,
                "VALOR($)": vl_hora * (175 / 100) * 4,
                "HOURS_FIELD": "4",
                "JORNAL_FIELD": False,
            },
        ],
        "DOMINGO NOCTURNO (18:00-6:00)": [
            {
                "HORA": "18:00 a 02:00",
                "DESCRIPCION": "Dominical",
                "CC-NOMINA": "1M02",
                "PORCENTAJE": 100,
                "VALOR($)": vl_dia * (100 / 100),
                "HOURS_FIELD": None,
                "JORNAL_FIELD": False,
            },
            {
                "HORA": "18:00 a 21:00",
                "DESCRIPCION": "3 - Horas diurnas dominicales",
                "CC-NOMINA": "1M06",
                "PORCENTAJE": 80,
                "VALOR($)": vl_hora * (80 / 100) * 3,
                "HOURS_FIELD": "3",
                "JORNAL_FIELD": False,
            },
            {
                "HORA": "21:00 a 24:00",
                "DESCRIPCION": "3 - Horas nocturnas dominicales",
                "CC-NOMINA": "1M07",
                "PORCENTAJE": 115,
                "VALOR($)": vl_hora * (115 / 100) * 3,
                "HOURS_FIELD": "3",
                "JORNAL_FIELD": False,
            },
            {
                "HORA": "18:00 a 00:00",
                "DESCRIPCION": "6 - Compensatorio lab.domingo",
                "CC-NOMINA": "1M08",
                "PORCENTAJE": 100,
                "VALOR($)": vl_hora * (100 / 100) * 6,
                "HOURS_FIELD": "6",
                "JORNAL_FIELD": False,
            },
            {
                "HORA": "00:00 a 02:00",
                "DESCRIPCION": "2 - Jornada nocturna ordinaria Recargo",
                "CC-NOMINA": "1MA1",
                "PORCENTAJE": 135,
                "VALOR($)": vl_hora * (135 / 100) * 2,
                "HOURS_FIELD": "2",
                "JORNAL_FIELD": False,
            },
            {
                "HORA": "02:00 a 06:00",
                "DESCRIPCION": "4 - Hora Extra Nocturna",
                "CC-NOMINA": "M305",
                "PORCENTAJE": 175,
                "VALOR($)": vl_hora * (175 / 100) * 4,
                "HOURS_FIELD": "4",
                "JORNAL_FIELD": False,
            },
        ],
        "DOMINGO DIURNO 8 HORAS FESTIVO (6:00-14:00)": [
            {
                "HORA": "06:00 a 14:00",
                "DESCRIPCION": "FESTIVO",
                "CC-NOMINA": "1M03",
                "PORCENTAJE": 100,
                "VALOR($)": vl_dia * (100 / 100),
                "HOURS_FIELD": None,
                "JORNAL_FIELD": False,
            },
            {
                "HORA": "06:00 a 14:00",
                "DESCRIPCION": "8 Hora Diurna Festiva (80%)",
                "CC-NOMINA": "1MAM",
                "PORCENTAJE": 80,
                "VALOR($)": vl_hora * (80 / 100) * 8,
                "HOURS_FIELD": "8",
                "JORNAL_FIELD": False,
            },
            {
                "HORA": "06:00 a 14:00",
                "DESCRIPCION": "8 Compensat lab. Festivo (100%)",
                "CC-NOMINA": "1MAO",
                "PORCENTAJE": 100,
                "VALOR($)": vl_hora * (100 / 100) * 8,
                "HOURS_FIELD": "8",
                "JORNAL_FIELD": False,
            },
        ],
        "DIA A BASICO 8 HORAS NOCHE (22:00-06:00)": [
            {
                "HORA": "22:00 a 06:00",
                "DESCRIPCION": "Jornal",
                "CC-NOMINA": "1MF9",
                "PORCENTAJE": 100,
                "VALOR($)": vl_dia * (100 / 100),
                "HOURS_FIELD": None,
                "JORNAL_FIELD": False,
            },
            {
                "HORA": "22:00 a 06:00",
                "DESCRIPCION": "8-Horas de Recargo Nocturno",
                "CC-NOMINA": "M220",
                "PORCENTAJE": 35,
                "VALOR($)": vl_hora * (35 / 100) * 8,
                "HOURS_FIELD": "8",
                "JORNAL_FIELD": False,
            },
        ],
        "DOMINGO 8 HORAS (14:00-22:00)": [
            {
                "HORA": "14:00 a 22:00",
                "DESCRIPCION": "DOMINICAL",
                "CC-NOMINA": "1M02",
                "PORCENTAJE": 100,
                "VALOR($)": vl_dia * (100 / 100),
                "HOURS_FIELD": None,
                "JORNAL_FIELD": False,
            },
            {
                "HORA": "14:00 a 21:00",
                "DESCRIPCION": "7- Horas Diurna Festiva (75%)",
                "CC-NOMINA": "1M06",
                "PORCENTAJE": 80,
                "VALOR($)": vl_hora * (80 / 100) * 7,
                "HOURS_FIELD": "7",
                "JORNAL_FIELD": False,
            },
            {
                "HORA": "21:00 a 22:00",
                "DESCRIPCION": "1 - Hora Noct Dominic (115%)",
                "CC-NOMINA": "1M07",
                "PORCENTAJE": 115,
                "VALOR($)": vl_hora * (115 / 100) * 1,
                "HOURS_FIELD": "1",
                "JORNAL_FIELD": False,
            },
            {
                "HORA": "14:00 a 22:00",
                "DESCRIPCION": "8 - Compensat lab. Festivo (100%)",
                "CC-NOMINA": "1M08",
                "PORCENTAJE": 100,
                "VALOR($)": vl_hora * (100 / 100) * 8,
                "HOURS_FIELD": "8",
                "JORNAL_FIELD": False,
            },
        ],
        "LUNES A VIERNES ORDINARIO 8 HORAS (14:00-22:00)": [
            {
                "HORA": "14:00 a 22:00",
                "DESCRIPCION": "JORNAL",
                "CC-NOMINA": "1MF9",
                "PORCENTAJE": 100,
                "VALOR($)": vl_dia * (100 / 100),
                "HOURS_FIELD": None,
                "JORNAL_FIELD": True,
            },
            {
                "HORA": "21:00 a 22:00",
                "DESCRIPCION": "1 Hora de Recargo Nocturno 35%",
                "CC-NOMINA": "M220",
                "PORCENTAJE": 35,
                "VALOR($)": vl_hora * (35 / 100) * 1,
                "HOURS_FIELD": "1",
                "JORNAL_FIELD": False,
            },
        ],
        "SABADO NOCTURNO (18:00-06:00)": [
            {
                "HORA": "18:00 a 02:00",
                "DESCRIPCION": "Jornal",
                "CC-NOMINA": "1MF9",
                "PORCENTAJE": 100,
                "VALOR($)": vl_dia * (100 / 100),
                "HOURS_FIELD": None,
                "JORNAL_FIELD": False,
            },
            {
                "HORA": "21:00 a 00:00",
                "DESCRIPCION": "3 Recargo Nocturno",
                "CC-NOMINA": "1M220",
                "PORCENTAJE": 35,
                "VALOR($)": vl_hora * (35 / 100) * 3,
                "HOURS_FIELD": "3",
                "JORNAL_FIELD": False,
            },
            {
                "HORA": "00:00 a 02:00",
                "DESCRIPCION": "2 Recargo Noct Festivo",
                "CC-NOMINA": "1M11",
                "PORCENTAJE": 35,
                "VALOR($)": vl_hora * (35 / 100) * 2,
                "HOURS_FIELD": "2",
                "JORNAL_FIELD": False,
            },
            {
                "HORA": "00:00 a 02:00",
                "DESCRIPCION": "2 Domingo o Festivo Noct",
                "CC-NOMINA": "1M12",
                "PORCENTAJE": 80,
                "VALOR($)": vl_hora * (80 / 100) * 2,
                "HOURS_FIELD": "2",
                "JORNAL_FIELD": False,
            },
            {
                "HORA": "02:00 a 06:00",
                "DESCRIPCION": "4 Horas Extra Noct Festiva  (80+175HEXT NO) 255%",
                "CC-NOMINA": "M315",
                "PORCENTAJE": 255,
                "VALOR($)": vl_hora * (255 / 100) * 4,
                "HOURS_FIELD": "4",
                "JORNAL_FIELD": False,
            },
        ],
        "DOMINGO A LUNES FESTIVO NOCTURNO (18:00-06:00)": [
            {
                "HORA": "18:00 a 02:00",
                "DESCRIPCION": "Dominical",
                "CC-NOMINA": "1M02",
                "PORCENTAJE": 100,
                "VALOR($)": vl_dia * (100 / 100),
                "HOURS_FIELD": None,
                "JORNAL_FIELD": False,
            },
            {
                "HORA": "18:00 a 21:00",
                "DESCRIPCION": "3 - Horas diurnas dominicales",
                "CC-NOMINA": "1M06",
                "PORCENTAJE": 80,
                "VALOR($)": vl_hora * (80 / 100) * 3,
                "HOURS_FIELD": "3",
                "JORNAL_FIELD": False,
            },
            {
                "HORA": "21:00 a 02:00",
                "DESCRIPCION": "5 - Horas nocturnas dominicales 115%",
                "CC-NOMINA": "1M07",
                "PORCENTAJE": 115,
                "VALOR($)": vl_hora * (115 / 100) * 5,
                "HOURS_FIELD": "5",
                "JORNAL_FIELD": False,
            },
            {
                "HORA": "18:00 a 02:00",
                "DESCRIPCION": "8 - Compensatorio lab.domingo",
                "CC-NOMINA": "1M08",
                "PORCENTAJE": 100,
                "VALOR($)": vl_hora * (100 / 100) * 8,
                "HOURS_FIELD": "8",
                "JORNAL_FIELD": False,
            },
            {
                "HORA": "02:00 a 06:00",
                "DESCRIPCION": "4 - Hora Extra Nocturna dominic (80+175) 255%",
                "CC-NOMINA": "M315",
                "PORCENTAJE": 255,
                "VALOR($)": vl_hora * (255 / 100) * 4,
                "HOURS_FIELD": "4",
                "JORNAL_FIELD": False,
            },
        ],
        "DIA DOMINGO HORAS NOCHE (22:00-6:00)": [
            {
                "HORA": "22:00 a 06:00",
                "DESCRIPCION": "Dominical",
                "CC-NOMINA": "1M02",
                "PORCENTAJE": 100,
                "VALOR($)": vl_dia * (100 / 100),
                "HOURS_FIELD": None,
                "JORNAL_FIELD": False,
            },
            {
                "HORA": "22:00 a 12:00",
                "DESCRIPCION": "2 - Horas Noct Dominical",
                "CC-NOMINA": "1M07",
                "PORCENTAJE": 115,
                "VALOR($)": vl_hora * (115 / 100) * 2,
                "HOURS_FIELD": "2",
                "JORNAL_FIELD": False,
            },
            {
                "HORA": "22:00 a 12:00",
                "DESCRIPCION": "2 - Compensatorio Lab Dominical",
                "CC-NOMINA": "1M08",
                "PORCENTAJE": 100,
                "VALOR($)": vl_hora * (100 / 100) * 2,
                "HOURS_FIELD": "2",
                "JORNAL_FIELD": False,
            },
            {
                "HORA": "12:00 a 06:00",
                "DESCRIPCION": "6 - Jornada Nocturna Dominical",
                "CC-NOMINA": "1MA1",
                "PORCENTAJE": 135,
                "VALOR($)": vl_hora * (135 / 100) * 6,
                "HOURS_FIELD": "6",
                "JORNAL_FIELD": False,
            },
        ],
        "DIA SABADO HORAS NOCHE (22:00-6:00)": [
            {
                "HORA": "22:00 a 06:00",
                "DESCRIPCION": "Jornal",
                "CC-NOMINA": "1MF9",
                "PORCENTAJE": 100,
                "VALOR($)": vl_dia * (100 / 100),
                "HOURS_FIELD": None,
                "JORNAL_FIELD": True,
            },
            {
                "HORA": "22:00 a 12:00",
                "DESCRIPCION": "2 - Hora de Recargo Nocturno",
                "CC-NOMINA": "M220",
                "PORCENTAJE": 35,
                "VALOR($)": vl_hora * (35 / 100) * 2,
                "HOURS_FIELD": "2",
                "JORNAL_FIELD": False,
            },
            {
                "HORA": "22:00 a 06:00",
                "DESCRIPCION": "6 - Recargo Noct Festivo",
                "CC-NOMINA": "1M11",
                "PORCENTAJE": 35,
                "VALOR($)": vl_hora * (35 / 100) * 6,
                "HOURS_FIELD": "6",
                "JORNAL_FIELD": False,
            },
            {
                "HORA": "22:00 a 06:00",
                "DESCRIPCION": "6 - Domingo o festivo Noct",
                "CC-NOMINA": "1M12",
                "PORCENTAJE": 80,
                "VALOR($)": vl_hora * (80 / 100) * 6,
                "HOURS_FIELD": "6",
                "JORNAL_FIELD": False,
            },
        ],
        "Hora ley 2101 de 2021": [
            {
                "HORA": "1 hora",
                "DESCRIPCION": "1-hora extra Nocturna Festiva  ley 2101",
                "CC-NOMINA": "1MCI",
                "PORCENTAJE": 255,
                "VALOR($)": vl_hora * (255 / 100) * 1,
                "HOURS_FIELD": "1",
                "JORNAL_FIELD": False,
            },
            {
                "HORA": "1 hora",
                "DESCRIPCION": "1-hora extra Dia ley 2101",
                "CC-NOMINA": "1MCG",
                "PORCENTAJE": 125,
                "VALOR($)": vl_hora * (125 / 100) * 1,
                "HOURS_FIELD": "1",
                "JORNAL_FIELD": False,
            },
            {
                "HORA": "1 hora",
                "DESCRIPCION": "1-hora extra Nocturna  ley 2101",
                "CC-NOMINA": "1MCH",
                "PORCENTAJE": 175,
                "VALOR($)": vl_hora * (175 / 100) * 1,
                "HOURS_FIELD": "1",
                "JORNAL_FIELD": False,
            },
        ],
    }

    # Return the data for the selected jornada
    return jornada_data.get(tipo_jornada, [])


def get_jornada_data_with_custom_hours(
    tipo_jornada, vl_dia, vl_hora, custom_hours, jornal_multiplier=1
):
    """
    Returns DataFrame data with custom hours and jornal multiplier applied
    custom_hours: dict with DESCRIPCION as key and custom hours as value
    jornal_multiplier: number to multiply jornal entries by
    """
    base_data = get_jornada_data(tipo_jornada, vl_dia, vl_hora)
    modified_data = []

    for row in base_data:
        new_row = copy.deepcopy(row)
        descripcion = row["DESCRIPCION"]

        # Handle jornal multiplier
        if row.get("JORNAL_FIELD", False):
            new_row["VALOR($)"] = row["VALOR($)"] * jornal_multiplier
            if jornal_multiplier != 1:
                new_row["DESCRIPCION"] = f"{descripcion} (x{jornal_multiplier})"

        # Handle custom hours
        elif row["HOURS_FIELD"] and descripcion in custom_hours:
            # Extract original hours from the HOURS_FIELD
            original_hours = int(row["HOURS_FIELD"])
            new_hours = custom_hours[descripcion]

            # Recalculate VALOR with new hours
            # Get the base calculation without the original hours multiplier
            base_valor_per_hour = row["VALOR($)"] / original_hours
            new_row["VALOR($)"] = base_valor_per_hour * new_hours

            # Update description to reflect new hours
            new_row["DESCRIPCION"] = descripcion.replace(
                str(original_hours), str(new_hours)
            )

        # Remove helper fields from final output
        new_row.pop("HOURS_FIELD", None)
        new_row.pop("JORNAL_FIELD", None)
        modified_data.append(new_row)

    return modified_data


def is_multi_day_jornada(jornada_name):
    """
    Determine if a jornada covers multiple days (needs "Cantidad de Horas" field)
    """
    multi_day_keywords = ["LUNES A SABADO", "LUNES A VIERNES", "Hora ley"]
    return any(keyword in jornada_name for keyword in multi_day_keywords)


# Streamlit app setup
st.set_page_config(
    page_title="Calculadora Provicosecha",
    layout="centered",
    page_icon="imgs/calc.ico",
)
st.title("Calculadora de Horas Extras")
st.image("imgs/banner.png", width=300)
st.divider()

# Create tabs
tab1, tab2 = st.tabs(["📊 Calculadora Individual", "📋 Calculadora Múltiple"])

with tab1:
    # Original single jornada calculator
    # Main form
    main_header_col1, main_header_col2 = st.columns([1, 1])

    with main_header_col1:
        with st.form("horas_extras_form"):
            st.subheader("**Datos Básicos**")

            # Input fields
            basico = st.number_input(
                "**BÁSICO**",
                min_value=0.0,
                value=st.session_state.basico,
                step=1000.0,
                format="%.2f",
                help="Salario básico del empleado",
            )

            divisor = st.number_input(
                "**DIVISOR**",
                min_value=1,
                value=st.session_state.divisor,
                step=1,
                help="Divisor para calcular valor hora (default: 220)",
            )

            tipo_jornada = st.selectbox(
                label="**TIPO JORNADA**",
                options=[
                    "LUNES A SABADO ORDINARIO DIURNO (06:00-18:00)",
                    "DOMINGO DIURNO (06:00-18:00)",
                    "LUNES A VIERNES ORDINARIO NOCTURNO (18:00-6:00)",
                    "DOMINGO NOCTURNO (18:00-6:00)",
                    "DOMINGO DIURNO 8 HORAS FESTIVO (6:00-14:00)",
                    "DIA A BASICO 8 HORAS NOCHE (22:00-06:00)",
                    "DOMINGO 8 HORAS (14:00-22:00)",
                    "LUNES A VIERNES ORDINARIO 8 HORAS (14:00-22:00)",
                    "SABADO NOCTURNO (18:00-06:00)",
                    "DOMINGO A LUNES FESTIVO NOCTURNO (18:00-06:00)",
                    "DIA DOMINGO HORAS NOCHE (22:00-6:00)",
                    "DIA SABADO HORAS NOCHE (22:00-6:00)",
                    "Hora ley 2101 de 2021",
                ],
                index=None,
                placeholder="Seleccionar tipo de jornada",
            )

            # Submit button
            col_left, col_center, col_right = st.columns([2, 2, 2])
            with col_center:
                submitted = st.form_submit_button("Calcular")

    # Results section
    with main_header_col2:
        with st.container(key="results", border=True):
            st.subheader("**Resultados**")

            basico_placeholder = st.empty()
            basico_placeholder.metric(label="BÁSICO", value="$0")
            # VL. DIA and VL. HORA in vertical layout
            vl_dia_placeholder = st.empty()
            vl_dia_placeholder.metric(label="VL. DIA", value="$0")

            vl_hora_placeholder = st.empty()
            vl_hora_placeholder.metric(label="VL. HORA", value="$0")

    # Process form submission
    if submitted:
        if basico <= 0:
            st.error("El valor del BÁSICO debe ser mayor a 0")
        elif divisor <= 0:
            st.error("El DIVISOR debe ser mayor a 0")
        elif tipo_jornada is None:
            st.error("Debe seleccionar un TIPO DE JORNADA")
        else:
            # Update session state
            st.session_state.basico = basico
            st.session_state.divisor = divisor

            # Calculate values
            vl_dia = basico / 30
            vl_hora = basico / divisor

            # Update metrics
            basico_placeholder.metric(label="**BÁSICO**", value=f"${basico:,.2f}")
            vl_dia_placeholder.metric(label="**VL. DIA**", value=f"${vl_dia:,.2f}")
            vl_hora_placeholder.metric(label="**VL. HORA**", value=f"${vl_hora:,.2f}")

    # DataFrame section
    st.header("Detalle de Horas por Jornada")

    if submitted and tipo_jornada:
        # Get data for selected jornada
        jornada_data = get_jornada_data(tipo_jornada, vl_dia, vl_hora)

        if jornada_data:
            st.subheader(f"**{tipo_jornada}**")

            # Create DataFrame structure (remove helper fields)
            df_jornada = pd.DataFrame(
                [
                    {
                        k: v
                        for k, v in row.items()
                        if k not in ["HOURS_FIELD", "JORNAL_FIELD"]
                    }
                    for row in jornada_data
                ]
            )

            # Calculate and show total
            total_valor = df_jornada["VALOR($)"].sum()
            st.metric("**TOTAL JORNADA**", f"${total_valor:,.2f}")

            # Configure column display
            column_config = {
                "HORA": st.column_config.TextColumn(
                    "HORA", help="Rango horario", width="small"
                ),
                "DESCRIPCION": st.column_config.TextColumn(
                    "DESCRIPCIÓN", help="Descripción del tipo de hora", width="medium"
                ),
                "CC-NOMINA": st.column_config.TextColumn(
                    "CC-NÓMINA", help="Código contable", width="small"
                ),
                "PORCENTAJE": st.column_config.NumberColumn(
                    "PORCENTAJE",
                    format="%d%%",
                    help="Porcentaje aplicado",
                    width="small",
                ),
            }

            # Display DataFrame for manual editing
            st.dataframe(
                df_jornada,
                use_container_width=True,
                column_config=column_config,
                hide_index=True,
                height=300,
            )
            st.success("Cálculo realizado exitosamente")

        else:
            st.info("No hay datos configurados para esta jornada")
    else:
        st.info("Complete el formulario y seleccione una jornada para ver el detalle")

with tab2:
    # New multi-jornada calculator
    st.header("Calculadora de Múltiples Jornadas")

    # Basic inputs (no form needed)
    st.subheader("**Datos Básicos**")

    col1, col2 = st.columns(2)
    with col1:
        basico_multi = st.number_input(
            "**BÁSICO**",
            min_value=0.0,
            value=st.session_state.basico,
            step=1000.0,
            format="%.2f",
            help="Salario básico del empleado",
            key="basico_multi",
        )

    with col2:
        divisor_multi = st.number_input(
            "**DIVISOR**",
            min_value=1,
            value=st.session_state.divisor,
            step=1,
            help="Divisor para calcular valor hora (default: 220)",
            key="divisor_multi",
        )

    # Jornada selection (outside form for immediate response)
    st.subheader("**Selección de Jornadas**")

    jornadas_disponibles = [
        "LUNES A SABADO ORDINARIO DIURNO (06:00-18:00)",
        "DOMINGO DIURNO (06:00-18:00)",
        "LUNES A VIERNES ORDINARIO NOCTURNO (18:00-6:00)",
        "DOMINGO NOCTURNO (18:00-6:00)",
        "DOMINGO DIURNO 8 HORAS FESTIVO (6:00-14:00)",
        "DIA A BASICO 8 HORAS NOCHE (22:00-06:00)",
        "DOMINGO 8 HORAS (14:00-22:00)",
        "LUNES A VIERNES ORDINARIO 8 HORAS (14:00-22:00)",
        "SABADO NOCTURNO (18:00-06:00)",
        "DOMINGO A LUNES FESTIVO NOCTURNO (18:00-06:00)",
        "DIA DOMINGO HORAS NOCHE (22:00-6:00)",
        "DIA SABADO HORAS NOCHE (22:00-6:00)",
        "Hora ley 2101 de 2021",
    ]

    selected_jornadas = st.multiselect(
        "**Seleccionar Jornadas a Calcular**",
        options=jornadas_disponibles,
        help="Puede seleccionar múltiples jornadas para calcular el total mensual",
        key="selected_jornadas_multi",
    )

    # Dynamic input fields based on selected jornadas (outside form)
    jornada_configs = {}

    if selected_jornadas:
        st.subheader("**Configuración por Jornada**")

        for jornada in selected_jornadas:
            st.write(f"**{jornada}**")

            if is_multi_day_jornada(jornada):
                # For multi-day jornadas, show "Cantidad de Horas" fields and jornal multiplier
                st.write("📝 *Jornada de múltiples días - Ajustar parámetros:*")

                # Jornal multiplier field
                jornal_multiplier = st.number_input(
                    f"Multiplicador de Jornal para {jornada}",
                    min_value=0.1,
                    value=1.0,
                    step=0.1,
                    format="%.1f",
                    help="Número por el cual multiplicar el valor del jornal",
                    key=f"jornal_{jornada}",
                )

                # Get sample data to identify which fields have hours
                sample_data = get_jornada_data(
                    jornada, 1, 1
                )  # Using 1,1 just to get structure
                hours_config = {}

                for row in sample_data:
                    if row.get("HOURS_FIELD"):
                        default_hours = int(row["HOURS_FIELD"])
                        descripcion = row["DESCRIPCION"]

                        hours_config[descripcion] = st.number_input(
                            f"Horas para: {descripcion}",
                            min_value=0,
                            value=default_hours,
                            step=1,
                            key=f"hours_{jornada}_{descripcion}",
                        )

                jornada_configs[jornada] = {
                    "type": "hours",
                    "config": hours_config,
                    "jornal_multiplier": jornal_multiplier,
                }
            else:
                # For single-day jornadas, show "Numero de Dias" field
                st.write("📅 *Jornada de día específico - Número de días:*")
                num_dias = st.number_input(
                    f"Número de días para {jornada}",
                    min_value=1,
                    value=1,
                    step=1,
                    key=f"dias_{jornada}",
                )

                jornada_configs[jornada] = {"type": "days", "config": num_dias}

            st.divider()

        # Calculate button (outside form for immediate response)
        if st.button("🧮 Calcular Total", use_container_width=True, type="primary"):
            submitted_multi = True
        else:
            submitted_multi = False
    else:
        submitted_multi = False

    # Process multi-jornada calculation
    if submitted_multi:
        if basico_multi <= 0:
            st.error("El valor del BÁSICO debe ser mayor a 0")
        elif divisor_multi <= 0:
            st.error("El DIVISOR debe ser mayor a 0")
        elif not selected_jornadas:
            st.error("Debe seleccionar al menos una jornada")
        else:
            # Calculate values
            vl_dia = basico_multi / 30
            vl_hora = basico_multi / divisor_multi

            # Show basic metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("**BÁSICO**", f"${basico_multi:,.2f}")
            with col2:
                st.metric("**VL. DIA**", f"${vl_dia:,.2f}")
            with col3:
                st.metric("**VL. HORA**", f"${vl_hora:,.2f}")

            st.header("**Resultados Detallados**")

            total_general = 0
            all_results = []

            for jornada in selected_jornadas:
                config = jornada_configs[jornada]

                if config["type"] == "hours":
                    # Multi-day jornada with custom hours and jornal multiplier
                    jornada_data = get_jornada_data_with_custom_hours(
                        jornada,
                        vl_dia,
                        vl_hora,
                        config["config"],
                        config["jornal_multiplier"],
                    )
                else:
                    # Single-day jornada with number of days multiplier
                    jornada_data = get_jornada_data(jornada, vl_dia, vl_hora)
                    # Remove helper fields
                    jornada_data = [
                        {
                            k: v
                            for k, v in row.items()
                            if k not in ["HOURS_FIELD", "JORNAL_FIELD"]
                        }
                        for row in jornada_data
                    ]

                # Calculate total for this jornada
                jornada_total = sum(row["VALOR($)"] for row in jornada_data)

                if config["type"] == "days":
                    # Multiply by number of days
                    num_dias = config["config"]
                    jornada_total *= num_dias
                    for row in jornada_data:
                        row["VALOR($)"] *= num_dias

                total_general += jornada_total

                # Display results for this jornada
                with st.expander(
                    f"**{jornada}** - Total: ${jornada_total:,.2f}", expanded=True
                ):
                    if config["type"] == "days":
                        st.info(f"📅 Calculado para {config['config']} día(s)")
                    elif config["type"] == "hours" and config["jornal_multiplier"] != 1:
                        st.info(
                            f"💼 Jornal multiplicado por {config['jornal_multiplier']}"
                        )

                    df_jornada = pd.DataFrame(jornada_data)

                    # Configure column display
                    column_config = {
                        "HORA": st.column_config.TextColumn(
                            "HORA", help="Rango horario", width="small"
                        ),
                        "DESCRIPCION": st.column_config.TextColumn(
                            "DESCRIPCIÓN",
                            help="Descripción del tipo de hora",
                            width="medium",
                        ),
                        "CC-NOMINA": st.column_config.TextColumn(
                            "CC-NÓMINA", help="Código contable", width="small"
                        ),
                        "PORCENTAJE": st.column_config.NumberColumn(
                            "PORCENTAJE",
                            format="%d%%",
                            help="Porcentaje aplicado",
                            width="small",
                        ),
                    }

                    st.dataframe(
                        df_jornada,
                        use_container_width=True,
                        column_config=column_config,
                        hide_index=True,
                        height=200,
                    )

                # Add to all results for summary
                for row in jornada_data:
                    row["JORNADA"] = jornada
                    all_results.append(row)

            # Show total general
            st.success(f"## **TOTAL GENERAL: ${total_general:,.2f}**")
