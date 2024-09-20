import folium
from langchain.agents import initialize_agent,AgentType
from langchain.tools import BaseTool
from pydantic import BaseModel,Field
from langchain.retrievers import WikipediaRetriever
from typing import Any,Type
from langchain.prompts import PromptTemplate
import streamlit as st
from langchain.chat_models import ChatOpenAI
from streamlit_folium import st_folium


class LLM:
    def __init__(self,key):
        self.llm = ChatOpenAI(
            temperature=0.5,
            open_api_key = key,
            model="gpt-3.5-turbo"
        )
    prompt = PromptTemplate.from_template(
    """
    당신은 세계사에 대해 잘 알고 있는 지원 어시스턴트입니다.
    당신은 반드시 아래의 예시의 형식에 맞추어 사건의 발생 위치에 대해서 대답해야합니다.

    예시1)
    사건명: 보스턴 차 사건
    사건 발생 위치: 42.3601,-71.0589 (미국 보스턴)

    예시2)
    사건명: 프랑스 혁명
    사건 발생 위치: 48.8566,2.3522 (프랑스 파리)

    예시3)
    사건명: 사라예보 사건
    사건 발생 위치: 43.8563,18.4131 (보스니아 헤르체고비나 사라예보)

    예시4)
    사건명: 제 1차 세계 대전
    사건 발생 위치: 전 세계

    사용자의 입력)
    {user_massage}
    """
    )

    def invoke_chain(self,text):
        chain = self.prompt | self.llm
        return chain.invoke({"user_massage":text})

###
def Wikipedia(keyword):
    rs = "위키피디아 검색 결과) \n\n"
    retriver = WikipediaRetriever(top_k_results=1, lang="ko")
    data_list = retriver.get_relevant_documents(keyword)
    for page_content in data_list:
        rs += f"{page_content.page_content} \n\n"
    return rs

class WikipediaToolArgsSchema(BaseModel):
    keyword: str = Field(description="'Search Keyword' to Use for Wikipedia Search")

class WikipediaTool(BaseTool):
    name = "Wikipedia"
    description = """
    A tool used by Wikipedia to search for specific keywords. Use 'keyword' as a parameter.
    """
    args_schema: Type[WikipediaToolArgsSchema] = WikipediaToolArgsSchema

    def _run(self, keyword):
        rs = Wikipedia(keyword)
        return rs
    
###
def draw_the_map(latitude,longitude):
    m = folium.Map(location=[latitude,longitude],
                   width='70px',
                   height='30px')
    folium.Marker([latitude,longitude],popup="Markder Location").add_to(m)
    return m

class foliumToolArgsSchema(BaseModel):
    latitude: str = Field(description="위도 값을 의미합니다.")
    longitude: str = Field(description="경도 값을 의미합니다.")

class foliumTool(BaseTool):
    name = "draw_the_map"
    description = """
    주어진 경도와 위도를 바탕으로 folium라는 라이브러리를 사용하여 지도를 그리는 도구입니다.
    """
    args_schema: Type[foliumToolArgsSchema] = foliumToolArgsSchema

    def _run(self, latitude,longitude):
        rs = draw_the_map(latitude,longitude)
        return rs