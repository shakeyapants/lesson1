def get_answer(question):
    question = question.lower()
    answers = {'hi' : 'Hey', 'how are you?' : 'Fine', 'bye' : 'See you'}
    return answers.get(question)

print(get_answer('bye'))