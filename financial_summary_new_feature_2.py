import streamlit as st
import PyPDF2
from pathlib import Path
from langchain.document_loaders import UnstructuredFileLoader
import openai


#retriving results from Cognitive search
# OPENAI_API_KEY = "0d9f51419bfa47d1910e6c61abafa7cd"
openai.api_type = "azure"
openai.api_base = "https://azureopenaitext.openai.azure.com/"
openai.api_version = "2023-09-15-preview"
# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = "6ad08c8e58dd4de9985b86b1209d9cc2"
from langchain.llms import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.chat_models import ChatOpenAI
import time



col1, col2 = st.columns([1, 3])
with col1:
    st.markdown(
        "![Alt Text](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHgAAAB+CAMAAADY4yX9AAAAilBMVEX///8AcK0Sq9sAbqwAqNoAZqgAaqoAaKkAptkAY6cAbKsSrt0ApNgAX6X7/f7O3erh6vLH2OcQn9GxyN7l8/qCyejy9/rp8PY1fbSqw9thk7+Z0eu23vBlv+Oq2u/L6PVNhriaudWOsNBUjr1tnMR4oscodbAHebQEgboSi8AOk8hPuOHa7/iCqczpSEsYAAAEkklEQVRoge2a2ZKiMBRAgbAviqIsbtBq49b+/+9NAu0ChCSQYFdNcV6m5qVP3TUBlKSRkZGRkf+byR95o3g1/RNvZujaIQj/wCvLMrDir8+qo9yWC4Cm7z+onnlAfgB06x59yLu35ArGZ6L2D5pcA2h5Mvh0JbJd9xZtls0G1YYrC6NF2NZxwFIHBi7cpzoZSOtnFmj3QqzMH0A72euEcEt0W3zQs1gjh1uircROVvStUcP9DRqIPDsSYLBpEeJ6zI8pTVXDOwrZJuG310kLMWIBhQ7yDll+YMu8cwUXc9dwS7PO12KJoffRyui05Njd/qFtMbOYjd7mL4txdFvQ+pn9uHHsdo65T50T+mKmm/XOB2V07NfMdXPXeZ7GPWYXh7HqtMMSzq56w/rq4D16orTIzNzaYcbbzRVAzthgvqjyPtBXTN5pLqy8D6yAJV5bxBRVAQa9s/1uBz4jxp3uHUAL8SiHsy++viX6kegNs75nLxWNeFocBc/RG8SQv4TujSoAtFd5qMYq0fat4lzwIAHE67952ywLTTSwT+fz5XI5n08PudayviJDXMD26TJXnAJFMa+lu21jfwvraCBfFSh84jjzE1oPGjbXvrBE26eKtnRfQduVU1jA9qWhRWYTLmxcX0eyoArbV5wX4sp2jBEngjKtt3lhtm0PU+RMzOEAWr3QfPaa+1rQ6Q+w9X1gYt4TBEIyDU4kr+Kcmt11FJNpkhZyba4QIWsazIkBQw717pqIuL/jB7iS60tdLORAPFG0KNf1B7iZgN7S53TxvC4W0NTgTEs0Tsy/twCtowvMhpj7hCCtrDeEi8GZRas49a7mr7HJJL7VxbxdTR/hAnVZ83LPMcMII8xdXcy5uXTqrixxF3Ux365mGmGE0/BKR56HNaAyZnrdFAcc89R6y2LItOT3j5hy+r9Qt00vvHP1LjJgOBxKMSZgjhXCnGhchSX0/btnvIwjrKiNrfXLvV972Wy7Eop/8F4p6nXBZe/oTYtXkvY9qvxcHdu1S/Y2luWLSfcqvybJCZckMyFeCf3OobP5WWA4Ku0xq0pK8sIn1Y5b5O0ejULaqfjV6W6xA/ye7LhTf72fScVW+rlhzKZDTHNJp0c3L7i9p7OYlo1TjVo1nR3TF4kpe2d7Sfg+SY9FnC4V13VVCPzHWVOK+2LG+MkHWIG0qewO8+kI090asmnbGC0xM2Vbl2eStK1WtHGD7IjP8K1YQz+5+Kl1UusyZiVcUQoNrDu6l2/rLazeeL+RBzppoDW5eJORNvcFdVHQg757Or7UwALle4ywObEK2hX8arv5jQ/oXhb8FhK3K8rBXacLrmKHyerkGajH0btfYOuWkd39x59sFPjNrSqOgr9tsBJN94c4znOQ53F2DPxn70wI3iLjjUeVHoSR7/tRJXmLljw/e4xhO/dhZxK99MOoH6lDvGu4N96+xrLYOKTLnereBsjyIl3fFJLWVbbpEL9T/FFcwgyZym0zTG3hEK1V3OVGVWGzLQezlmyW8Hw31QcmOuy364Glv0zgMb8sgGd9+hHlyMjIyMjIyED8Ax/ZVkQ3zARGAAAAAElFTkSuQmCC)")
with col2:
    st.title("Financial Report Summarization")
    st.write("Generative AI")
output = None
def main():
    try:

        file_path = st.file_uploader("Choose a file", type=["pdf"])
        print("Filepath: ", file_path)
        pdf_folder = 'C:/Users/GALONE/Downloads/Gen_ai_report_summarization'
        global pdf_path
        pdf_path = Path(pdf_folder, file_path.name)
        #print("save_path:-", Save_path)
        with open(pdf_path, mode='wb') as w:
            w.write(file_path.getvalue())

        pdf_reader = PyPDF2.PdfReader(file_path)

        # Get the total number of pages
        global total_pages
        total_pages = len(pdf_reader.pages)


        # Display the total number of pages on the UI
        st.write(f"Total Pages in PDF: {total_pages}")
        global start_page
        start_page = st.number_input("Start Page", value=1, min_value=1, max_value=total_pages)
        global end_page
        end_page = st.number_input("End Page", value=total_pages, min_value=1, max_value=total_pages)


    except Exception as e:
        pass


if __name__ == "__main__":
  main()


def write_strings_to_txt(strings, save_path):

    """Writes a list of strings to a text file at a particular path.

    Args:
    strings: A list of strings to write to the text file.
    save_path: The path to the text file to write to.
    """

    with open(save_path, "w") as file:
        file.write("\n".join(strings))


options = ["Revenue", "Profitability", "Financial performance", "Growth by industry vertical", "Geographic market growth", "Earning per share", "Equity & Liabilities", "expenses", "Assets", "Other Parameter"]

# Create a multiple select box
selected_options = st.multiselect("Select Financial Parameters:", options)

# Check if the list is empty
if "Other Parameter" in selected_options:
    question = st.text_input("Enter the parameter of your choice", value="", type="default")
    question_list = question.split(", ")
    for value in question_list:
        selected_options.append(value)

    # Create a new list that contains all of the selected options except for the "Other Parameter" option.
    summary_options = []
    for option in selected_options:
        if option != "Other Parameter":
            summary_options.append(option)

    save_path = "C:/Users/GALONE/Downloads/Gen_ai_report_summarization/Topic_list.txt"
    write_strings_to_txt(summary_options, save_path)
else:
    # Save the selected options to a text file.
    save_path = "C:/Users/GALONE/Downloads/Gen_ai_report_summarization/Topic_list.txt"
    write_strings_to_txt(selected_options, save_path)


with st.form("Question"):

    if submitted := st.form_submit_button("Submit"):
        llm=ChatOpenAI(engine="gpt-35-turbo",openai_api_key="6ad08c8e58dd4de9985b86b1209d9cc2")
        chain = load_summarize_chain(llm=llm, chain_type='map_reduce',verbose=True) # verbose=True optional to see what is getting sent to the LLM

        output_path = r"C:/Users/GALONE/Downloads/Gen_ai_report_summarization/output.pdf"

        def extract_pages(pdf_path,start_page,end_page, output_path):

            print("pdf_path:",pdf_path,start_page,end_page, output_path)
            with open(pdf_path, "rb") as f:

                pdf_reader = PyPDF2.PdfReader(f)
                pdf_writer = PyPDF2.PdfWriter()

                for page_num in range(start_page - 1, end_page):

                    pdf_writer.add_page(pdf_reader.pages[page_num])

                with open(output_path, "wb") as o:

                    pdf_writer.write(o)

        extract_pages(pdf_path, start_page, end_page, output_path)

        loader = UnstructuredFileLoader(r"C:/Users/GALONE/Downloads/Gen_ai_report_summarization/output.pdf")

        documents = loader.load()
        whole_docu=documents[0].page_content


        def summarizer(text_to_summarize):
            with open(r"C:/Users/GALONE/Downloads/Gen_ai_report_summarization/Topic_list.txt", 'r') as file:
                text = file.read()
                sys_0=f""" You are an AI Assistant. You will be given a document and a topic list
        
                    As an AI assistant you have two task:

                    Task 1: Extract the relevant information related to each topic and make a representative summary for each topic  
        
                     Task2: For the part of the document which is not related to the topics mentioned in the topic list, give an appropriate topic name and              its representative summary. 
        
                    """

                user_1 = f"""Given below is the "Topic list" and a document based on which you will be performing
        
                    Task-1 and Task 2: 
        
                    Topic list: {text}        
                    Document for which you will be creating a representative summary for each topic:{text_to_summarize}
                    The format of your answer will the following:
                    2. Topic List Name: Representative summary for that topic

                    Guidelines to follow while extracting information:
        
                    1. Always quote the exact number and KPIs as mentioned in the page
                    2. Do not generate or draw conclusion from the page only make summary using the facts mentioned in the documents       
                    3. Use bulletpoints where applicable
                    4. Use numbers mentioned in the document."""

                summary = openai.ChatCompletion.create(engine="gpt-35-turbo", messages = [{"role":"system","content":sys_0}, {"role":"user", "content":user_1}], temperature=0 , stop=None)
                return summary

        text_splitter = RecursiveCharacterTextSplitter(
            # Set a really_small chunk size, just to show.
            chunk_size = 18000,
            chunk_overlap  = 450,
            length_function = len,
            #add_start_index = True,
        )
        texts = text_splitter.create_documents([whole_docu])
        print("len:- ",len(texts))
        summarized_content=[]
        for x in texts:
            summarized_content.append(summarizer(x.page_content))
            time.sleep(5)

        summary_list=[]
        for x in summarized_content:
            summary_list.append(x.choices[0].message.content)

        final_docu="\nSummary of a single document\n"+"\nSummary of a single document\n".join(summary_list)

        num_tokens=llm.get_num_tokens(final_docu)
        print(num_tokens)

        def final_summarizer(text_to_summarize):

            with open(r"C:/Users/GALONE/Downloads/Gen_ai_report_summarization/Topic_list.txt", 'r') as file:
                text = file.read()
            sys_0=f""" You are an AI Assistant. You will be given a list of summary of documents based on a topic list.
            As an AI assistant you have one task where you will use these summaries to create one single summary, the final summary 
            be focused on a given list of topics.
            """

            user_1 = f""" Given below is the list of document summaries and a topic list, which you will use to provide one final summary that will focus on the given topic list and topics that are present in each summary. 
            
            List of document summaries: {text_to_summarize}
            
            Also, here is the Topic list which the final summary will focus on along with topics that are present in each summary: {text}
            
            The Format of your final answer will be: "Topic List Name (the Topic list name should come in Bold)
            
            Representative summary of that topic"
            
            Guidelines to follow while extracting information:
            
            1. Always quote the exact numbers and KPIs as mentioned in the list of document summaries.
            
            2. Extract numeric data, graphs, tabular data related to financial parameters when applicable.
            
            3. If the user requests relationships among parameters, analyze and present any relevant correlations or connections among the mentioned parameters.
            
            4. Do not generate or draw conclusions from the list of document summaries; only make summaries using the facts mentioned in the documents.
            
            5. Use bulletpoints where applicable.
            
            6. Use numbers mentioned in the list of document summaries in the final summary."""
            summary= openai.ChatCompletion.create(
            engine="gpt-35-turbo",
            messages = [{"role":"system","content":sys_0},{"role":"user","content":user_1}],
            temperature=0,
            stop=None)
            return summary


        if(num_tokens>4000):
            time.sleep(5)
            chain_document=text_splitter.create_documents([final_docu])
            output = chain.run(chain_document)
            st.write(output)
        else:
            time.sleep(5)
            response=final_summarizer(final_docu)
            output=response.choices[0].message.content
            st.write(output)

if output is None:
    output = b''  # Provide an empty binary data as the default

# Add a download button for the generated output text
st.download_button(
    label="Download Output Text",
    data=output,  # The output text you want to download
    file_name="output.txt",  # The name of the downloaded file
    key="output_download_button",
)



