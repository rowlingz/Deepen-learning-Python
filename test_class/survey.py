# -*- coding:utf-8 -*-


class AnonymousSurvey():
    """收集匿名调查问卷的答案"""

    def __init__(self, question):
        """储存问题，并储存对应问题的答案"""
        self.question = question
        self.responses = []

    def show_question(self):
        print(self.question)

    def store_response(self, new_response):
        self.responses.append(new_response)

    def show_results(self):
        print("Survey results: ")
        for response in self.responses:
            print("- " + response)


# question = "What language did you first learn to speak?"
# my_survey = AnonymousSurvey(question)
#
# my_survey.show_question()
