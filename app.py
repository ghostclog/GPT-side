import streamlit as st
import folium
import llmAndAgent
from streamlit_folium import st_folium
# 웹 페이지 설정
st.set_page_config(
    page_title="GPT with Map",
    page_icon="🌍",
)

# 세션 초기화 영역
if 'agent' not in st.session_state:
    st.session_state.agent = None
if 'text' not in st.session_state:
    st.session_state.text = None


    

st.title("Map with GPT")
if (st.session_state.text == None):
    st.markdown("""
        특정 사건 사고. 혹은 도시나 국가에 대해 물어보시면, 해당 사건 사고의 중심이 되는. 국가의 수도인. 아니면, 질문하신 도시의 위치를 지도에 표시해드리겠습니다. 그리고, 질문에 대한 답을 드리겠습니다.
        모든 답변은 위키피디아를 중심으로 답변을 드리며, 위키피디아에 공지되어 있지 않을 경우 답변을 받을 수 없거나, 부정확 할 수도 있습니다.
        """)

with st.sidebar:
    st.write("깃허브 레포지토리 링크: https://github.com/ghostclog")
    api_key = st.text_input("사용하실 open api 키를 입력해주세요.")
    if api_key:
        llm = llmAndAgent.LLM(api_key)
        if llm:
            st.session_state.agent = llmAndAgent.Agent(llm.llm)
if st.session_state.agent:
    st.session_state.text = st.text_input("질문을 시작하세요!")
    if st.session_state.text:
        rs = llm.invoke_chain(st.session_state.text)
        print()
        if("전 세계" not in rs.content):
           with st.spinner("지도 생성 중..."):
            st.session_state.agent.map_invoke(rs.content)
        with st.spinner("내용 생성 중..."):
            contents = st.session_state.agent.normal_invoke(rs.content)["output"]
            st.write(contents)
      
