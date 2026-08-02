from germany_decoded.assistant import Assistant

def main():
    assistant = Assistant()
    question = "Can I reduce my rent because my apartment has defects?"

    result = assistant.ask(question)
    print(result["answer"])
    #print(assistant.last_call.id)

if __name__ == "__main__":
    main()