from crewai import Crew, Agent, Task, Process
from crewai_tools import SerperDevTool
from langchain_openai.chat_models import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings

from dotenv import load_dotenv
import os
import streamlit as st
import streamlit.components.v1 as components

load_dotenv()
search_tool = SerperDevTool()

llm = AzureChatOpenAI(
    model_name="gpt-35-turbo",
    openai_api_version=os.environ.get("OPENAI_API_VERSION"),
    azure_deployment=os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
)


def provide_guidance(product_name):
    # define agents
    print(product_name)

    market_research_analyst = Agent(
        role="Market Research Analyst",
        goal=f"""Analyze the market demand for {product_name} and 
                    suggest marketing strategies""",
        backstory=f"""Expert at understanding market demand, target audience, 
                        and competition for products like {product_name}. 
                        Skilled in developing marketing strategies 
                        to reach a wide audience.""",
        verbose=True,
        allow_delegation=True,
        tools=[search_tool],
        llm=llm,
    )

    technology_expert = Agent(
        role="Technology Expert",
        goal=f"Assess technological feasibilities and requirements for producing high-quality {product_name}",
        backstory=f"""Visionary in current and emerging technological trends, 
                        especially in products like {product_name}. 
                        Identifies which technologies are best suited 
                        for different business models.""",
        verbose=True,
        allow_delegation=True,
        tools=[search_tool],
        llm=llm,
    )

    business_consultant = Agent(
        role="Business Development Consultant",
        goal=f"""Evaluate the business model for {product_name}, 
                focusing on scalability and revenue streams""",
        backstory=f"""Seasoned in shaping business strategies for products like {product_name}. 
                        Understands scalability and potential 
                        revenue streams to ensure long-term sustainability.""",
        verbose=True,
        allow_delegation=True,
        tools=[search_tool],
        llm=llm,
    )


    # define task1
    task1 = Task(
        description=f"""Analyze the market demand for {product_name}. Current month is Jan 2024.
                            Write a report on the ideal customer profile and marketing 
                            strategies to reach the widest possible audience. 
                            Include at least 10 bullet points addressing key marketing areas.""",
        expected_output="Report on market demand analysis and marketing strategies.",
        agent=market_research_analyst,
        tools=[search_tool],
    )

    # define task2
    task2 = Task(
        description=f"""Assess the technological aspects of manufacturing 
                        high-quality {product_name}. Write a report detailing necessary 
                        technologies and manufacturing approaches. 
                        Include at least 10 bullet points on key technological areas.""",
        expected_output="Report on technological aspects of manufacturing.",
        agent=technology_expert,
        tools=[search_tool],
    )

    # define task3
    task3 = Task(
        description=f"""Summarize the market and technological reports 
                        and evaluate the business model for {product_name}. 
                        Write a report on the scalability and revenue streams 
                        for the product. Include at least 10 bullet points 
                        on key business areas. Give Business Plan, 
                        Goals and Timeline for the product launch. Current month is Jan 2024.""",
        expected_output="Report on business model evaluation and product launch plan.",
        agent=business_consultant,
    )

    # Create and Run the Crew
    product_crew = Crew(
        agents=[market_research_analyst, technology_expert, business_consultant],
        tasks=[task1, task2, task3],
        verbose=2,
        process=Process.sequential,
        memory=True,
        cache=True,
        max_rpm=100,
        share_crew=True,
        embedder={
            "provider": "azure_openai",
            "config": {
                "model": "text-embedding-ada-002",
                "deployment_name": "Embedding",
            },
        },
    )

    crew_result = product_crew.kickoff()
    return crew_result


# Streamlit UI
def main():

    st.set_page_config(page_title="Custom Business Product Guide", page_icon=":bulb:")

    # set title
    st.title("CUSTOM BUSINESS PRODUCT GUIDE")

    # Markdown
    st.subheader(""":red[Great] :orange[minds] :green[discuss] :blue[ideas], :violet[average] :gray[minds] :rainbow[discuss] :red[events], :orange[small] :green[minds] :rainbow[discuss] :red[people]""")

    guidance=""
    # sidebar
    with st.sidebar:
        st.header("Enter the business product idea:")
        product_name = st.text_input("Idea:")
        
        if st.button("Get Guidance"):
            if not product_name:
                st.info("Please enter your product name")
            else:
                guidance = provide_guidance(product_name)
    # st.text_area("")
    st.success(guidance)

    st.markdown(
    """
    <style>
    body {
        background-color: #f0f0f0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if __name__ == "__main__":
    main()
