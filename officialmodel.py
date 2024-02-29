import google.generativeai as genai 
import os
import flask


class BardGenerator:
    def __init__(self):
        genai.configure(api_key="AIzaSyAplxTGM7nlWUplp86mQbiPJvCVZBCpgZM")
        self.text_model = genai.GenerativeModel("gemini-pro")
        self.image_model = genai.GenerativeModel("gemini-pro-vision")
        self.questions = {}
    
    def format_text_mcq(self, text):
        # print(text)
        question = text[text.find("Question:")+len("Question:"):text.find('A')]
        if ("Choices" in text): options = text[text.find("Choices:")+len("Choices:"):text.find("Answer:")]
        else: options = text[text.find("A)"):text.find("Answer:")]
        answer = text[text.find("Answer:")+len("Answer:"):]
        question = question.replace("*", ''); answer = answer.replace("*", ''); options = options.replace('*', '')
        question = question.replace("\n", ''); answer = answer.replace('\n', ''); # options = options.replace("\n", ' ')
        question = question.strip(); answer = answer.strip()
        # print(question, options, answer, sep="\n")
        self.questions["Question"] = question
        self.questions['Options'] = options
        self.questions["Answer"] = answer
    
    def format_text_single_word(self, text):
        question = question = text[text.find("Question:")+len("Question:"):text.find('?')]
        answer = text[text.find("Answer:")+len("Answer:"):]
        question = question.replace("*", ''); answer = answer.replace("*", '')
        question = question.replace("\n", ''); answer = answer.replace('\n', '')
        question = question.strip(); answer = answer.strip()
        self.questions["Question"] = question
        self.questions["Answer"] = answer

    def generate_questions_from_text_single_word(self, topic, difficulty="college"):
        single_word_response = self.text_model.generate_content(f"Give me 1 question that can be answered in a single sentence of {difficulty} difficulty with no choices on the topic {topic} and the answer to the question in the following example format: \
                            Question: What is the capital of France?\nAnswer: Paris. Provide the response in plain text without any markdown formatting.") 
        text = single_word_response.text
        # print(text)
        self.format_text_single_word(text)
    def generate_questions_from_text_mcq(self, topic, difficulty="college"):
        mcq_response = self.text_model.generate_content(f"Give me 1 multiple choice question of {difficulty} difficulty with 4 choices on the topic {topic} and the answer to the question in the following example format: \
                            Question: What is the capital of France?\nA) Paris\nB) Beijing\nC) Delhi\nD) Kingston\nAnswer: A) Paris. Provide the response in plain text without any markdown formatting.")
        text = mcq_response.text
        # print(text)
        self.format_text_mcq(text)

    
# bard = BardGenerator() 
# bard.generate_questions_from_text_single_word("Memory Structure and Architecture of Computers")
# # bard.generate_questions_from_text_mcq("Formula one racing history")
# print("\n", bard.questions)


    



