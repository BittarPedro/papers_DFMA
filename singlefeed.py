import streamlit as st

def get_queries(author_name: str, include_abbrev: bool = False) -> str:
    author_name_list = author_name.split(' ')
    author_name_query = '+'.join(author_name_list)
    if include_abbrev:
        abbrev_name = author_name.split(' ')
        abbrev_name = [abbrev[0] if index != len(abbrev_name) - 1 else abbrev for index, abbrev in enumerate(abbrev_name)]
        abbrev_name_query = '+'.join(abbrev_name)
        return '%22+OR+au:%22'.join([author_name_query, abbrev_name_query])
    else:
        return author_name_query

# Streamlit app
st.title("Gerar feed de artigos do DFMA")
st.write("Faça o upload do arquivo CSV contendo os nomes dos autores para gerar um feed RSS do ArXiv.")

# File uploader
uploaded_file = st.file_uploader("Upload authors.csv", type="csv")

if uploaded_file is not None:
    try:
        # Read the uploaded file
        authorlist = uploaded_file.read().decode("utf-8").splitlines()
        
        # Generate the full query
        full_query = '%22+OR+au:%22'.join(map(get_queries, authorlist))
        
        # Generate the RSS feed URL
        rss_feed_url = f'http://export.arxiv.org/api/query?search_query=au:%22{full_query}%22&sortBy=submittedDate&sortOrder=descending&max_results=100'
        
        # Display the RSS feed URL
        st.success("O seu RSS feed foi gerado!")
        st.write("O seu feed é:")
        st.code(rss_feed_url, language="text")
        
        # Provide a clickable link
        st.markdown(f"[Abrir feed no browser]({rss_feed_url})")
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
else:
    st.info("Por favor faça o upload do arquivo CSV.")
