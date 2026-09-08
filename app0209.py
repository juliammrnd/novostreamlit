import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

df = pd.read_csv("domicilios.csv", sep=";", decimal=",")


st.set_page_config(
page_title="Dashboard de Dados",
layout="wide"
)
st.title("Dashboard de Dados - Tecnologia")

st.markdown("**Desenvolvido por:** Ana Clara Luz Lira e Júlia Monteiro Miranda")

st.markdown("**2CDD01**")

st.markdown("**Fonte dos dados: TIC Domicílios — NIC.br/Cetic.br.**")

arquivo = st.file_uploader(
"Envie um arquivo CSV",
type=["csv"]
)
st.markdown("### Aula 1")

st.markdown("**Pergunta 1:** Qual é a porcentagem de domicílios com computador em cada classe social?")

st.markdown("**Pergunta 2:** Entre os lares que não têm internet, a barreira financeira (preço do serviço ou do aparelho) supera a barreira geográfica (falta de disponibilidade do serviço na região)?")

if arquivo is not None:
    df = pd.read_csv(arquivo, sep=';', decimal=',')
    colunas_interesse = [
        'RENDA_FAMILIAR', 'CLASSE_2015', 'A2_A_FAIXA', 'A2_B_FAIXA',
        'A1_EXCLUSIVOS', 'A4_COB', 'A5_A', 'A5_B', 'A5_C', 'A5_D', 'A5_E'
    ]
    colunas_presentes = [col for col in colunas_interesse if col in df.columns]
    df = df[colunas_presentes]
    df = df.replace([99, 999999999], np.nan)
    
    st.subheader("Visualização dos dados")
    st.dataframe(df.head())
    
    import io 
    
    st.subheader("Informações da Base de Dados (df.info)")

    buffer = io.StringIO()

    df.info(buf=buffer)

    resumo = buffer.getvalue()

    st.text(resumo)
    
    
    st.dataframe(df.describe())
    
    col1, col2 = st.columns(2)
    col1.metric(
        "Quantidade de registros",
        df.shape[0]
    )
    col2.metric(
        "Quantidade de colunas",
        df.shape[1]
    )

    df.isnull().sum()
    df.duplicated().sum()
    df.dtypes
    
    st.subheader("1. Acesso a computadores por Classe Social")
    
    df['TEM_COMPUTADOR'] = (df['A2_A_FAIXA'] > 0) | (df['A2_B_FAIXA'] > 0)
    
    
    df_grafico1 = df.groupby('CLASSE_2015')['TEM_COMPUTADOR'].mean().reset_index()
    df_grafico1['TEM_COMPUTADOR'] = df_grafico1['TEM_COMPUTADOR'] * 100 # Transforma em porcentagem
    
  
    fig1 = px.bar(
        df_grafico1, 
        x='CLASSE_2015', 
        y='TEM_COMPUTADOR',
        title="Porcentagem de domicílios com computador por Classe",
        labels={'CLASSE_2015': 'Classe Social', 'TEM_COMPUTADOR': 'Possui Computador (%)'},
        text_auto='.1f' # Mostra o número na barra com 1 casa decimal
    )
    
    st.plotly_chart(fig1, use_container_width=True)
    
    st.markdown("""
    **O que podemos observar?**
    Os dados mostram uma desigualdade expressiva no acesso a computadores de acordo com a classe social. Enquanto quase a totalidade dos domicílios da classe A possui o equipamento, esse número cai drasticamente nas classes C e D/E.
    """)
    
   
    st.divider()
    st.subheader("Indicadores Gerais")
    
 
    media_geral_computador = df['TEM_COMPUTADOR'].mean() * 100
    
    col_ind1, col_ind2 = st.columns(2)
    col_ind1.metric("Média de domicílios com computador", f"{media_geral_computador:.1f}%")
    
   
    lares_sem_internet = df['A5_A'].dropna().shape[0]
    col_ind2.metric("Total de domicílios sem acesso à internet", lares_sem_internet)

    
    st.divider()
    st.subheader("2. Barreiras Financeiras vs Geográficas (Domicílios sem Internet)")
    
   
    barreira_financeira = df['A5_A'].sum() + df['A5_B'].sum()
    barreira_geografica = df['A5_C'].sum()
    
    
    dados_motivos = pd.DataFrame({
        'Tipo de Barreira': ['Financeira (Serviço/Aparelho Caro)', 'Geográfica (Sem cobertura na região)'],
        'Quantidade de Domicílios': [barreira_financeira, barreira_geografica]
    })
    
   
    fig2 = px.bar(
        dados_motivos, 
        x='Tipo de Barreira', 
        y='Quantidade de Domicílios',
        title="O que mais impede o acesso à internet?",
        color='Tipo de Barreira', # Pinta cada barra de uma cor diferente
        text_auto=True # Mostra o número exato na barra
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("""
    **O que podemos observar?**
    Para os lares que não possuem acesso à internet, a barreira financeira (custo do serviço ou do aparelho) é um impeditivo muito maior do que a barreira geográfica (falta de disponibilidade do serviço na região).
    """)
    
    st.divider()

    st.markdown("""
    ### Análise Detalhada dos Resultados

    **1. Qual informação aparece?**  
    No primeiro gráfico, as informações tratam da relação entre acesso a computadores e a classe social. Já no segundo, o foco é o motivo da falta de acesso à internet.

    **2. Qual é o maior valor?**  
    O maior valor visível é a porcentagem de acesso a computadores na Classe A, que ultrapassa os 90%.

    **3. Existe algum valor muito diferente?**  
    Sim, podemos perceber uma discrepância enorme em relação ao acesso a computadores quando comparamos a Classe A (mais rica) com a Classe D/E (mais vulnerável).

    **4. Existe aumento ou diminuição?**  
    No primeiro gráfico, há uma clara diminuição da porcentagem de computadores nas residências à medida que a classe social cai; quanto mais baixa a classe, menor a porcentagem de domicílios com computador. No segundo gráfico, destaca-se que a barreira financeira supera amplamente a geográfica como impeditivo para o uso da internet.

    **5. Existem diferenças entre categorias?**  
    No gráfico 1, existe uma desigualdade muito grande: os números despencam das Classes A e B em comparação às Classes C e D/E. No gráfico 2, nota-se que há muito mais pessoas barradas por dificuldades financeiras do que por problemas de cobertura (geográfica).

    **6. Existe algum padrão aparente?**  
    Sim. Quanto menor a renda e a classe social da residência, menores são as chances de essa família ter um computador e acessar a internet.
    
    **7. Onde a IA nos ajudou?**
    A IA nos auxiliou na hora de achar um banco de dados sobre o tema de nosso interesse e no momento de produção da parte de programação do site, explicando onde estava os erros e sugerindo possíveis soluções
    """)
    
    st.divider()

    st.markdown("""
    ### Sobre o Projeto

    **1. O que investigamos?**  
    Este projeto investiga o cenário de acesso à tecnologia e à internet nos domicílios brasileiros. O foco da análise é responder a duas questões centrais: a disparidade no acesso a computadores entre as distintas classes sociais e, para os lares sem conexão à internet, se o principal obstáculo é a barreira financeira (custo de equipamentos/serviços) ou a barreira geográfica (falta de cobertura na região).

    **2. Qual base utilizamos?**  
    A análise foi construída a partir dos microdados da pesquisa **TIC Domicílios** (arquivo `domicilios.csv`), que mapeia o acesso às tecnologias de informação e comunicação no Brasil.

    **3. O que os dados mostraram?**  
    Os resultados mostram uma diferença significativa no acesso à tecnologia entre as classes sociais. Há uma desigualdade expressiva na posse de computadores: enquanto a Classe A apresenta mais de 90% de acesso, as Classes D/E registram menos de 6%. Em relação à conectividade, os dados comprovam que o fator financeiro impede o acesso à internet para o dobro de domicílios quando comparado à limitação geográfica.

    **4. Onde a Inteligência Artificial ajudou?**  
    A IA foi utilizada como ferramenta de apoio no desenvolvimento deste dashboard nas seguintes etapas:
    * **Resolução de Erros e Estruturação:** Identificação e correção do erro de leitura (`ParserError`) ao ajustar os parâmetros de separador e decimal do CSV.
    * **Limpeza e Tratamento de Dados:** Substituição de códigos de preenchimento da pesquisa (como `99` e `999999999` para "não sabe/não respondeu") por valores nulos (`NaN`), garantindo a precisão estatística dos gráficos.
    * **Síntese de Resultados:** Apoio na estruturação da análise visual em textos descritivos e objetivos, traduzindo os dados do Plotly em informações diretas.
    """)
        
    
    

