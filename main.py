import streamlit as st
import os
import pandas as pd
import altair as alt
# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Finanzas",
    page_icon="💰",
    layout="wide"
)
st.title('Dashboard de Finanzas Personales')

#Dataframe
df = pd.read_excel('BBDBancos.xlsx', sheet_name='BBDD')


# Filtramos por mes y año
add_selectbox_month, add_selectbox_year = st.columns(2)
with add_selectbox_month:
    add_selectbox_month = st.selectbox(
        'Mes',
        df['Mes'].drop_duplicates().sort_values()
    )
with add_selectbox_year:
    add_selectbox_year = st.selectbox(
        'Año',
        df['Año'].drop_duplicates().sort_values()
    )

df_filtered = df[(df['Mes'] == add_selectbox_month) & (df['Año'] == add_selectbox_year)]

if add_selectbox_month == 1:
    df_filtered_delta = df[(df['Mes'] == 12) & (df['Año'] == (add_selectbox_year - 1))]
else:
    df_filtered_delta = df[(df['Mes'] == (add_selectbox_month - 1)) & (df['Año'] == add_selectbox_year)]

st.write(df_filtered)

# --- MÉTRICAS PRINCIPALES ---
delta1 = (df_filtered[df_filtered['Tipo Movimiento'] == 'Ingreso']['Importe (€)'].sum().round(2)) - (df_filtered_delta[df_filtered_delta['Tipo Movimiento'] == 'Ingreso']['Importe (€)'].sum().round(2))
delta2 = (df_filtered[df_filtered['Tipo Movimiento'] == 'Gasto']['Importe (€)'].sum().round(2)) - (df_filtered_delta[df_filtered_delta['Tipo Movimiento'] == 'Gasto']['Importe (€)'].sum().round(2))
delta3 = (df_filtered['Importe (€)'].sum().round(2)) - (df_filtered_delta['Importe (€)'].sum().round(2))

col1, col2, col3 = st.columns(3)
col1.metric(label="Total Ingresos", value=df_filtered[df_filtered['Tipo Movimiento'] == 'Ingreso']['Importe (€)'].sum().round(2), delta=delta1.round(2))
col2.metric(label="Total Gastos", value=df_filtered[df_filtered['Tipo Movimiento'] == 'Gasto']['Importe (€)'].sum().round(2), delta=delta2.round(2))
col3.metric(label="Balance", value=df_filtered['Importe (€)'].sum().round(2), delta=delta3.round(2))


# --- 1. GRÁFICO POR CATEGORÍA (Ancho Completo) ---

st.write('### Detalle por Categoría')

df_cat = df_filtered.groupby('Categoría')['Importe (€)'].sum().round(2).reset_index()

bars_cat = alt.Chart(df_cat).mark_bar().encode(
    x=alt.X('Categoría:N', sort='-y',title=None),
    y=alt.Y('Importe (€):Q', title='Importe (€)'),
    color=alt.condition(
        alt.datum['Importe (€)'] >= 0,
        alt.value('#4CAF50'),
        alt.value('#F44336')
    )
)

text_cat_pos = bars_cat.mark_text(
    align='center', baseline='bottom', dy=-6
).encode(
    text=alt.Text('Importe (€):Q', format=',.2f')
).transform_filter(alt.datum['Importe (€)'] >= 0)

text_cat_neg = bars_cat.mark_text(
    align='center', baseline='top', dy=6
).encode(
    text=alt.Text('Importe (€):Q', format=',.2f')
).transform_filter(alt.datum['Importe (€)'] < 0)

chart_cat = (bars_cat + text_cat_pos + text_cat_neg).properties(height=350).configure_axis(grid=False)
st.altair_chart(chart_cat, use_container_width=True)


# --- 2. COLUMNAS PARA MOVIMIENTO Y BANCO ---

col_movimiento, col_banco = st.columns(2)

# --- COLUMNA IZQUIERDA: Tipo Movimiento ---
with col_movimiento:
    st.write('### Detalle por Tipo Movimiento')
    
    df_mov = df_filtered.groupby('Tipo Movimiento')['Importe (€)'].sum().round(2).reset_index()
    
    bars_mov = alt.Chart(df_mov).mark_bar().encode(
        x=alt.X('Tipo Movimiento:N', sort='-y',title=None),
        y=alt.Y('Importe (€):Q', title='Importe (€)'),
        color=alt.condition(
            alt.datum['Importe (€)'] >= 0,
            alt.value('#4CAF50'),
            alt.value('#F44336')
        )
    )
    
    text_mov_pos = bars_mov.mark_text(
        align='center', baseline='bottom', dy=-6
    ).encode(
        text=alt.Text('Importe (€):Q', format=',.2f')
    ).transform_filter(alt.datum['Importe (€)'] >= 0)
    
    text_mov_neg = bars_mov.mark_text(
        align='center', baseline='top', dy=6
    ).encode(
        text=alt.Text('Importe (€):Q', format=',.2f')
    ).transform_filter(alt.datum['Importe (€)'] < 0)
    
    chart_mov = (bars_mov + text_mov_pos + text_mov_neg).properties(height=350).configure_axis(grid=False)
    st.altair_chart(chart_mov, use_container_width=True)


# --- COLUMNA DERECHA: Banco ---
with col_banco:
    st.write('### Detalle por Banco')
    
    df_banco = df_filtered.groupby('Cuenta')['Importe (€)'].sum().round(2).reset_index()
    
    colores_entidades = {
        'Caixa': '#0054A6',
        'Hive5': '#F5A623',
        'ING': '#FF6200',
        'Manuel': '#9C27B0',
        'Mintos': '#00BFA5',
        'MyInvestor': '#00BCD4',
        'Trade Republic': '#1C1C1C'
    }
    color_por_defecto = '#D3D3D3'
    
    cuentas_presentes = df_banco['Cuenta'].unique()
    colores_personalizados = [colores_entidades.get(cuenta, color_por_defecto) for cuenta in cuentas_presentes]
    
    bars_banco = alt.Chart(df_banco).mark_bar().encode(
        x=alt.X('Cuenta:N', sort='-y',title=None),
        y=alt.Y('Importe (€):Q', title='Importe (€)'),
        color=alt.Color(
            'Cuenta:N',
            scale=alt.Scale(domain=list(cuentas_presentes), range=colores_personalizados),
            legend=None
        )
    )
    
    text_banco_pos = bars_banco.mark_text(
        align='center', baseline='bottom', dy=-6
    ).encode(
        text=alt.Text('Importe (€):Q', format=',.2f')
    ).transform_filter(alt.datum['Importe (€)'] >= 0)
    
    text_banco_neg = bars_banco.mark_text(
        align='center', baseline='top', dy=6
    ).encode(
        text=alt.Text('Importe (€):Q', format=',.2f')
    ).transform_filter(alt.datum['Importe (€)'] < 0)
    
    chart_banco = (bars_banco + text_banco_pos + text_banco_neg).properties(height=350).configure_axis(grid=False)
    st.altair_chart(chart_banco, use_container_width=True)