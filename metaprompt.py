import streamlit as st

from model_loading import ModelLoader
from utils import login
import resources

from langchain.schema import HumanMessage, AIMessage

model_loader = ModelLoader()

METAPROMPT = resources.metaprompt_texts["claude"]["template"]
REPLACEVARIABLES = resources.metaprompt_texts["claude"]["replace_vars"]

def chat_respond(chat_model,prompt):
    messages = [HumanMessage(content=prompt)]
    response = chat_model.invoke(messages).content
    return response


def generate_prompt(chat_model,task,metaprompt,variables=None):
    metaprompt = metaprompt.replace("{{TASK}}", task)

    prompt = chat_respond(chat_model,metaprompt)

    if variables is not None:
        prompt = add_variables_to_prompt(prompt, variables)

    replaced_prompt = None

    if variables is not None:
        replaced_prompt = replace_variables(chat_model,prompt, REPLACEVARIABLES, variables)

    return prompt,replaced_prompt


def add_variables_to_prompt(prompt, variables):
    variable_string = ""
    for variable in variables:
        variable_string += "\n{$" + variable.upper() + "}"
    # assistant_partial = f'\n<Instructions Structure>\n<Inputs>\n{variable_string}</Inputs>\n</Instructions Structure>'
    prompt = prompt.replace("<Inputs>", "<Inputs>" + variable_string)

    return prompt

def replace_variables(chat_model,prompt, remove_floating_variables_prompt, variables):
    # query = remove_floating_variables_prompt.format(PROMPT=prompt, VARIABLES=variables)
    query = remove_floating_variables_prompt.replace("{{PROMPT}}", prompt)
    # query = query.replace("{{VARIABLES}}", variables)

    response = chat_respond(chat_model,query)
    # return extract_between_tags("prompt", response, strip=True)[0]
    return response

st.title("Open Metaprompt - Prompt generator")

st.write("Select model loading type:")
selection_options = ['Hugginface Model Repository', 'OpenAI Model']
selection = st.selectbox("Model Loading Type", selection_options)

if selection == 'Hugginface Model Repository':

    # user_info = login.hf_login()
    
    hf_token = st.text_input("Enter Hugginface Token:",type="password",placeholder="hf_...")
    # hf_token = user_info.get('access_token')
    model_name = st.text_input("Enter Model Name:", placeholder="mistralai/Mistral-7B-Instruct-v0.1")
    tokens = st.slider("Max tokens", min_value=1, max_value=30000, value=1000, step=10)
    if hf_token and model_name:
        chat_model = model_loader.load_huggingface(hf_token,model_name,max_new_tokens=tokens)
        st.success(f"Model '{model_name}' loaded successfully!", icon="✅")

elif selection == 'OpenAI Model':
    # model_loader.load_from_openai()
    st.write("OpenAI Model not implemented yet.")

task = st.text_input("Enter the task:", value="Create an email to resolve a customer complaint")
variables = st.text_area("Enter the variables (comma separated):", value="CUSTOMER_COMPLAINT, COMPANY_NAME")

if st.button("Generate Prompt"):
    variables_list = [var.strip() for var in variables.split(",")]
    prompt_template, replaced_prompt = generate_prompt(chat_model, task, METAPROMPT, variables_list)
    
    # Display results
    st.subheader("Template Prompt")
    st.text_area("Template Prompt", prompt_template, height=200)
    
    st.subheader("Replaced Prompt")
    st.text_area("Replaced Prompt", replaced_prompt, height=200)

# Additional content
st.write("Based on Antrophic Claude's metaprompt notebook.")