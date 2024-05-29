import streamlit as st
import streamlit_auth0
import os

# Configure Auth0
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')  # Your Hugging Face OAuth Client ID
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')  # Your Hugging Face OAuth Client Secret
AUTH0_DOMAIN = 'huggingface.co'  # Your Hugging Face OAuth Domain

user_info = streamlit_auth0.login_button(client_id=AUTH0_CLIENT_ID, domain=AUTH0_DOMAIN)

# # Start the Auth0 authentication process
# auth0.start_login_button(label='Login with Hugging Face')

# # If authenticated, get the user information
# if auth0.authenticated:
#     user_info = auth0.get_user_info()
#     st.write(f'Hello, {user_info["nickname"]}!')
#     st.write(user_info)

#     # Token management
#     huggingfacehub_api_token = user_info['access_token']

#     # Example usage of the token to load a model or make API calls
#     st.write("Authenticated with Hugging Face")
#     # ... Load and use your Hugging Face models here using the `huggingfacehub_api_token` ...
# else:
#     st.write("Please login to use the app.")

# # Define the main app logic
# def main():
#     st.title("Hugging Face OAuth in Streamlit")

#     # Your main app code goes here
#     if auth0.authenticated:
#         model_name = st.text_input("Enter Model Name:")
#         if model_name:
#             st.write(f"Using model: {model_name}")
#             # Example function that uses the authenticated token
#             st.write("You can now make authenticated requests to Hugging Face API.")
#             # ... Your code to load and use the model ...

# if __name__ == "__main__":
#     main()

def hf_login():
    # Configure Auth0
    AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')  # Your Hugging Face OAuth Client ID
    AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')  # Your Hugging Face OAuth Client Secret
    AUTH0_DOMAIN = 'huggingface.co'  # Your Hugging Face OAuth Domain

    user_info = streamlit_auth0.login_button(client_id=AUTH0_CLIENT_ID, domain=AUTH0_DOMAIN)
    return user_info