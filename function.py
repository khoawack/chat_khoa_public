import openai
import prompt
def askGPT(text):
    openai.api_key = 'YOUR API KEY HERE'
    response = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = f"Using this information, pretend you are this person and if you dont know something say I dont know :{prompt.about_me()} to answer this question: {text}?",
        temperature = 0.1,
        max_tokens = 150,
    )
    return response.choices[0].text

# def main():
#     while True:
#         print('GPT: Ask me a question\n')
#         myQn = input()
#         askGPT(myQn)
#         print('\n')

# main()
