# 💰 Calculadora de Horas Extras - Providencia Cosecha S.A.

## 📌 Descripción
Esta aplicación es una **calculadora laboral** que permite calcular de forma precisa y automática las **horas extras**, **recargos nocturnos**, **trabajo dominical** y **trabajo festivo** según la legislación laboral colombiana. Desarrollada en **Python** con **Streamlit**, proporciona una interfaz sencilla e intuitiva para el área de nómina y recursos humanos.

## 🚀 Características
✅ Cálculo automático de horas extras diurnas y nocturnas.<br>
✅ Soporte para **9 tipos de jornadas laborales** diferentes.<br>
✅ Interfaz interactiva con **Streamlit**.<br>
✅ Códigos de nómina integrados para cada concepto.<br>
✅ Cálculo en tiempo real basado en salario básico.<br>
✅ Cumplimiento total con la **legislación laboral colombiana**.<br>

## 🛠 Tecnologías Utilizadas
- **Python 3.7+**
- **Streamlit 1.42.1**
- **Pandas 2.2.3** (para manipulación de datos)
- **Otras dependencias** (ver `requirements.txt` para lista completa)

## 🔧 Instalación y Uso

### Opción 1: Uso rápido desde escritorio
1. Hacer doble clic en el icono del escritorio
2. Se abre automáticamente en el navegador
3. ¡Listo para usar!

### Opción 2: Instalación local (paso a paso)

1. **Clonar o descargar los archivos**:
   ```sh
   git clone [URL_DEL_REPOSITORIO]
   cd calculadora-horas-extras
   ```

2. **Instalar Python (si no lo tienes)**:
   - Ir a: https://www.python.org/downloads/
   - Descargar Python (versión más reciente)
   - Instalar marcando "Add Python to PATH"
   - Reiniciar la computadora

3. **Crear un entorno virtual (opcional, recomendado)**:
   ```sh
   python -m venv venv
   source venv/bin/activate  # En Mac/Linux
   venv\Scripts\activate     # En Windows
   ```

4. **Instalar dependencias**:
   ```sh
   pip install -r requirements.txt
   ```

5. **Ejecutar la aplicación**:
   ```sh
   streamlit run app.py
   ```

6. **Abrir en navegador**:
   - Se abre automáticamente en: `http://localhost:8501`

## 📋 Jornadas Disponibles

### Jornadas Regulares
- **Lunes a Sábado - Día (6:00 AM - 6:00 PM)**
- **Lunes a Viernes - Noche (6:00 PM - 6:00 AM)**
- **Jornada 8 horas día (2:00 PM - 10:00 PM)**
- **Jornada 8 horas noche (10:00 PM - 6:00 AM)**

### Trabajo en Domingo
- **Domingo completo día (6:00 AM - 6:00 PM)**
- **Domingo completo noche (6:00 PM - 6:00 AM)**
- **Domingo medio turno (6:00 AM - 2:00 PM)**
- **Domingo tarde (2:00 PM - 10:00 PM)**

### Trabajo en Sábado Noche
- **Sábado noche (6:00 PM - 6:00 AM)**

## 🤝 Contribuciones
¡Las contribuciones son bienvenidas! Si deseas mejorar esta aplicación, abre un **Pull Request** o reporta un problema en **Issues**.

---
🏢 **Desarrollado para Providencia Cosecha S.A.**

🚀 **Viviana Andrea Martinez**