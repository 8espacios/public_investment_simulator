import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

inflation = .04 # https://datosmacro.expansion.com/ipc-paises/mexico
return_8espacios = .25
return_cetes = .0969 # https://www.cetesdirecto.com/sites/portal/inicio
return_bank_savings = .04 # Cuenta Ahorro Flexible HSBC (https://www.rankia.mx/blog/mejores-cuentas-mexico/2738108-mejores-cuentas-ahorro)
return_stock_bmv = -.0330 # https://www.spglobal.com/spdji/en/indices/equity/sp-bmv-ipc/#overview
years = [0,1,2,3,4,5,6,7,8,9,10]


@st.cache(show_spinner=True)
def update_investment_table(initial_amount):
    chart_data = pd.DataFrame({
        '8 Espacios': initial_amount * np.power((1 + return_8espacios - inflation), years),
        'CETES 1 año': initial_amount * np.power((1 + return_cetes - inflation), years),
        'Cuenta de ahorro': initial_amount * np.power((1 + return_bank_savings - inflation), years),
        'Bolsa Mexicana de Valores': initial_amount * np.power((1 + return_stock_bmv - inflation), years)
    })
    return chart_data.round(2)


st.title(f'¿Cuanto quieres invertir?')

initial_amount_slider = st.slider('Desliza para definir tu monto inicial', 
    min_value=50, 
    max_value=500, 
    step=5, 
    value=50,
    format=f'$%dK')

fig = px.line(update_investment_table(initial_amount_slider * 1000),
    labels = {
        'index':'Año de inversión',
        'value':'Monto inicial + intereses',
        'variable':'Instrumento'
    }
)

fig.update_traces(line=dict(width=3))

fig.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01
))

st.plotly_chart(fig, config=dict(displayModeBar=False), use_container_width=True)

st.table(update_investment_table(initial_amount_slider * 1000))