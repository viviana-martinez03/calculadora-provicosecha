import pandas as pd
import streamlit as st

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

    # Complete data structure - all 9 jornadas configured with direct formulas
    jornada_data = {
        "LUNES A SABADO ORDINARIO DIURNO (06:00-18:00)": [
            {
                "HORA": "06:00 a 14:00",
                "DESCRIPCION": "Jornal",
                "CC-NOMINA": "1MF9",
                "PORCENTAJE": 100,
                "VALOR($)": vl_dia * (100 / 100),
            },
            {
                "HORA": "14:00 a 18:00",
                "DESCRIPCION": "4 - Horas extras Diurnas",
                "CC-NOMINA": "M300",
                "PORCENTAJE": 125,
                "VALOR($)": vl_hora * (125 / 100) * 4,
            },
        ],
        "DOMINGO DIURNO (06:00-18:00)": [
            {
                "HORA": "06:00 a 14:00",
                "DESCRIPCION": "Dominical",
                "CC-NOMINA": "1M02",
                "PORCENTAJE": 100,
                "VALOR($)": vl_dia * (100 / 100),
            },
            {
                "HORA": "06:00 a 14:00",
                "DESCRIPCION": "8 - Horas diurnas dominicales",
                "CC-NOMINA": "1M06",
                "PORCENTAJE": 80,
                "VALOR($)": vl_hora * (80 / 100) * 8,
            },
            {
                "HORA": "06:00 a 14:00",
                "DESCRIPCION": "8 - Compensatorio lab.doming",
                "CC-NOMINA": "1M08",
                "PORCENTAJE": 100,
                "VALOR($)": vl_hora * (100 / 100) * 8,
            },
            {
                "HORA": "14:00 a 18:00",
                "DESCRIPCION": "4 - Hora Extra Diurna dominical (125+80)  205%",
                "CC-NOMINA": "M310",
                "PORCENTAJE": 205,
                "VALOR($)": vl_hora * (205 / 100) * 4,
            },
        ],
        "LUNES A VIERNES ORDINARIO NOCTURNO (18:00-6:00)": [
            {
                "HORA": "18:00 a 02:00",
                "DESCRIPCION": "Jornal",
                "CC-NOMINA": "1MF9",
                "PORCENTAJE": 100,
                "VALOR($)": vl_dia * (100 / 100),
            },
            {
                "HORA": "21:00 a 02:00",
                "DESCRIPCION": "5 - Recargo Nocturno",
                "CC-NOMINA": "M220",
                "PORCENTAJE": 35,
                "VALOR($)": vl_hora * (35 / 100) * 5,
            },
            {
                "HORA": "02:00 a 06:00",
                "DESCRIPCION": "4 - Hora Extra Nocturna",
                "CC-NOMINA": "M305",
                "PORCENTAJE": 175,
                "VALOR($)": vl_hora * (175 / 100) * 4,
            },
        ],
        "DOMINGO NOCTURNO (18:00-6:00)": [
            {
                "HORA": "18:00 a 02:00",
                "DESCRIPCION": "Dominical",
                "CC-NOMINA": "1M02",
                "PORCENTAJE": 100,
                "VALOR($)": vl_dia * (100 / 100),
            },
            {
                "HORA": "18:00 a 21:00",
                "DESCRIPCION": "3 - Horas diurnas dominicales",
                "CC-NOMINA": "1M06",
                "PORCENTAJE": 80,
                "VALOR($)": vl_hora * (80 / 100) * 3,
            },
            {
                "HORA": "21:00 a 24:00",
                "DESCRIPCION": "3 - Horas nocturnas dominicales",
                "CC-NOMINA": "1M07",
                "PORCENTAJE": 115,
                "VALOR($)": vl_hora * (115 / 100) * 3,
            },
            {
                "HORA": "18:00 a 00:00",
                "DESCRIPCION": "6 - Compensatorio lab.domingo",
                "CC-NOMINA": "1M08",
                "PORCENTAJE": 100,
                "VALOR($)": vl_hora * (100 / 100) * 6,
            },
            {
                "HORA": "00:00 a 02:00",
                "DESCRIPCION": "2 - Jornada nocturna ordinaria Recargo",
                "CC-NOMINA": "1MA1",
                "PORCENTAJE": 135,
                "VALOR($)": vl_hora * (135 / 100) * 2,
            },
            {
                "HORA": "02:00 a 06:00",
                "DESCRIPCION": "4 - Hora Extra Nocturna",
                "CC-NOMINA": "M305",
                "PORCENTAJE": 175,
                "VALOR($)": vl_hora * (175 / 100) * 4,
            },
        ],
        "DOMINGO DIURNO 8 HORAS FESTIVO (6:00-14:00)": [
            {
                "HORA": "06:00 a 14:00",
                "DESCRIPCION": "FESTIVO",
                "CC-NOMINA": "1M03",
                "PORCENTAJE": 100,
                "VALOR($)": vl_dia * (100 / 100),
            },
            {
                "HORA": "06:00 a 14:00",
                "DESCRIPCION": "8 Hora Diurna Festiva (80%)",
                "CC-NOMINA": "1MAM",
                "PORCENTAJE": 80,
                "VALOR($)": vl_hora * (80 / 100) * 8,
            },
            {
                "HORA": "06:00 a 14:00",
                "DESCRIPCION": "8 Compensat lab. Festivo (100%)",
                "CC-NOMINA": "1MAO",
                "PORCENTAJE": 100,
                "VALOR($)": vl_hora * (100 / 100) * 8,
            },
        ],
        "DIA A BASICO 8 HORAS NOCHE (22:00-06:00)": [
            {
                "HORA": "22:00 a 06:00",
                "DESCRIPCION": "Jornal",
                "CC-NOMINA": "1MF9",
                "PORCENTAJE": 100,
                "VALOR($)": vl_dia * (100 / 100),
            },
            {
                "HORA": "22:00 a 06:00",
                "DESCRIPCION": "8-Horas de Recargo Nocturno",
                "CC-NOMINA": "M220",
                "PORCENTAJE": 35,
                "VALOR($)": vl_hora * (35 / 100) * 8,
            },
        ],
        "DOMINGO 8 HORAS (14:00-22:00)": [
            {
                "HORA": "14:00 a 22:00",
                "DESCRIPCION": "DOMINICAL",
                "CC-NOMINA": "1M02",
                "PORCENTAJE": 100,
                "VALOR($)": vl_dia * (100 / 100),
            },
            {
                "HORA": "14:00 a 21:00",
                "DESCRIPCION": "7- Horas Diurna Festiva (75%)",
                "CC-NOMINA": "1M06",
                "PORCENTAJE": 80,
                "VALOR($)": vl_hora * (80 / 100) * 7,
            },
            {
                "HORA": "21:00 a 22:00",
                "DESCRIPCION": "1 - Hora Noct Dominic (115%)",
                "CC-NOMINA": "1M07",
                "PORCENTAJE": 115,
                "VALOR($)": vl_hora * (115 / 100) * 1,
            },
            {
                "HORA": "14:00 a 22:00",
                "DESCRIPCION": "8 - Compensat lab. Festivo (100%)",
                "CC-NOMINA": "1M08",
                "PORCENTAJE": 100,
                "VALOR($)": vl_hora * (100 / 100) * 8,
            },
        ],
        "LUNES A VIERNES ORDINARIO 8 HORAS (14:00-22:00)": [
            {
                "HORA": "14:00 a 22:00",
                "DESCRIPCION": "JORNAL",
                "CC-NOMINA": "1MF9",
                "PORCENTAJE": 100,
                "VALOR($)": vl_dia * (100 / 100),
            },
            {
                "HORA": "21:00 a 22:00",
                "DESCRIPCION": "1 Hora de Recargo Nocturno 35%",
                "CC-NOMINA": "M220",
                "PORCENTAJE": 35,
                "VALOR($)": vl_hora * (35 / 100) * 1,
            },
        ],
        "SABADO NOCTURNO (18:00-06:00)": [
            {
                "HORA": "18:00 a 02:00",
                "DESCRIPCION": "Jornal",
                "CC-NOMINA": "1MF9",
                "PORCENTAJE": 100,
                "VALOR($)": vl_dia * (100 / 100),
            },
            {
                "HORA": "21:00 a 00:00",
                "DESCRIPCION": "3 Recargo Nocturno",
                "CC-NOMINA": "1M220",
                "PORCENTAJE": 35,
                "VALOR($)": vl_hora * (35 / 100) * 3,
            },
            {
                "HORA": "00:00 a 02:00",
                "DESCRIPCION": "2 Recargo Noct Festivo",
                "CC-NOMINA": "1M11",
                "PORCENTAJE": 35,
                "VALOR($)": vl_hora * (35 / 100) * 2,
            },
            {
                "HORA": "00:00 a 02:00",
                "DESCRIPCION": "2 Domingo o Festivo Noct",
                "CC-NOMINA": "1M12",
                "PORCENTAJE": 80,
                "VALOR($)": vl_hora * (80 / 100) * 2,
            },
            {
                "HORA": "02:00 a 06:00",
                "DESCRIPCION": "4 Horas Extra Noct Festiva  (80+175HEXT NO) 255%",
                "CC-NOMINA": "M315",
                "PORCENTAJE": 255,
                "VALOR($)": vl_hora * (255 / 100) * 4,
            },
        ],
        "DOMINGO A LUNES FESTIVO NOCTURNO (18:00-06:00)": [
            {
                "HORA": "18:00 a 02:00",
                "DESCRIPCION": "Dominical",
                "CC-NOMINA": "1M02",
                "PORCENTAJE": 100,
                "VALOR($)": vl_dia * (100 / 100),
            },
            {
                "HORA": "18:00 a 21:00",
                "DESCRIPCION": "3 - Horas diurnas dominicales",
                "CC-NOMINA": "1M06",
                "PORCENTAJE": 80,
                "VALOR($)": vl_hora * (80 / 100) * 3,
            },
            {
                "HORA": "21:00 a 02:00",
                "DESCRIPCION": "5 - Horas nocturnas dominicales 115%",
                "CC-NOMINA": "1M07",
                "PORCENTAJE": 115,
                "VALOR($)": vl_hora * (115 / 100) * 5,
            },
            {
                "HORA": "18:00 a 02:00",
                "DESCRIPCION": "8 - Compensatorio lab.domingo",
                "CC-NOMINA": "1M08",
                "PORCENTAJE": 100,
                "VALOR($)": vl_hora * (100 / 100) * 8,
            },
            {
                "HORA": "02:00 a 06:00",
                "DESCRIPCION": "4 - Hora Extra Nocturna dominic (80+175) 255%",
                "CC-NOMINA": "M315",
                "PORCENTAJE": 255,
                "VALOR($)": vl_hora * (255 / 100) * 4,
            },
        ],
    }

    # Return the data for the selected jornada
    return jornada_data.get(tipo_jornada, [])


# Streamlit app setup
st.set_page_config(
    page_title="Calculadora Provicosecha",
    layout="centered",
    page_icon="imgs/calc.ico",
)
st.title("Calculadora de Horas Extras")
st.image("imgs/banner.png", width=300)
st.divider()

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

        # Create DataFrame structure
        df_jornada = pd.DataFrame(jornada_data)

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
                "PORCENTAJE", format="%d%%", help="Porcentaje aplicado", width="small"
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
