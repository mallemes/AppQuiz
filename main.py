arr = [1, 2, 3]

print(arr[0])
# class CreateQuizView(TemplateView):
#     template_name = "create.html"
#
#     def post(self, request, *args, **kwargs):
#         data = request.POST
#         name_quiz = data.get('name_quiz')
#         author = request.user
#         text_question_list = data.getlist("text_question[]")
#         text_answer_list = data.getlist("text_answer[]")
#         isTrueList = data.getlist("isTrue[]")
#         myIstruees = []
#         if text_question_list is not None and text_answer_list is not None and isTrueList is not None and name_quiz:
#             count = 4
#             myIstruees.append(int(isTrueList[0]))
#             for i in range(1, len(isTrueList)):
#                 myIstruees.append(int(isTrueList[i]) + count)
#                 count += 4
#             quiz = Quiz(name=name_quiz, author=author)
#             quiz.save()
#             sum = 0
#             for i in range(0, len(text_question_list)):
#                 que = Question(questionText=text_question_list[i], quiz=quiz)
#                 que.save()
#                 for j in range(sum, sum + 4):
#                     if myIstruees[i] - 1 == j:
#                         ans = Answer(question=que, textAnswer=text_answer_list[j], isCorrect=True)
#                         ans.question = que
#                         ans.textAnswer = text_answer_list[j]
#                         ans.isCorrect = True
#                         ans.save()
#                     else:
#                         ans = Answer()
#                         ans.question = que
#                         ans.textAnswer = text_answer_list[j]
#                         ans.isCorrect = False
#                         ans.save()
#                 sum = sum + 4
#
#         return redirect('index')
# {'name_quiz': ['quiz1'],
#         'text_question[]': ['Qazaqstan astanasy', 'question2'],
#         'text_answer[]': ['1text', '2text', '3text', '4text', 'answer2 - 1', 'answer2 - 2', 'answer2 - 3', 'answer2 - 4'],
#         'isTrue[]': ['1 ', '2']}

# {"name_quiz": "quiz1",
#  "text_question[]": ["Qazaqstan astanasy", "question2"],
#  "text_answer[]": ["1text-true", "2text", "3text", "4text", "answer2 - 1", "answer2 - 2", "answer2 - 3 true", "answer2 - 4"],
#  "isTrue[]": ["0", "2"]
#  }

{
"name_quiz": "quiz1 - API",
 "text_question[]": ["Qazaqstan astanasy API"],
 "text_answer[]": ["1text-true api", "2text api", "3text api", "4text api"],
 "isTrue[]": [0]
 }
