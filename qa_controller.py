
from operator import itemgetter

from langchain.chains import create_sql_query_chain
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.language_models import BaseChatModel 
from langchain_community.utilities import SQLDatabase

# TODO try agents https://python.langchain.com/v0.1/docs/use_cases/sql/quickstart/#agents
class QAService:
    def __init__(self, llm: BaseChatModel, db: SQLDatabase):
        self.llm = llm
        self.db = db

        answer_prompt = PromptTemplate.from_template(
            """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

        Question: {question}
        SQL Query: {query}
        SQL Result: {result}
        Answer: """
        )

        execute_query = QuerySQLDataBaseTool(db=db)
        write_query: Runnable = create_sql_query_chain(llm, db)

        db_chain = RunnablePassthrough.assign(query=write_query).assign(
            result=itemgetter("query") | execute_query
        )

        answer_chain = answer_prompt | llm | StrOutputParser()

        self.chain = db_chain | answer_chain

    def answer(self, question):
        return self.chain.invoke({"question": question})


class QAController:
    def __init__(self, qa_service:QAService):
        self.qa_service = qa_service

    def answer(self, question):
        return self.qa_service.answer(question)