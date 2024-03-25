import openai

if __name__ == "__main__":
    # Set your OpenAI API key here
    openai.api_key = "sk-GES9I1Q6uj7hXCGy21F1Dd68929c48159a8165780eC1274e"

    try:
        # Attempt to list available models as a way to validate the API key
        response = openai.Model.list()
        # If the above line does not raise an exception, the API key is valid
        print("API key is valid.")
    except Exception as e:
        # Catch other possible exceptions and print them
        print(f"An error occurred: {e}")
