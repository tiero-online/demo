# from django import forms
#
# from tests.models import Test, Question
# from .models import Task

# from django_select2.forms import ModelSelect2Widget, ModelSelect2MultipleWidget
#
#
# class MySelect2Widget(ModelSelect2Widget):
#     queryset = Test.objects.filter()
#     model = Test
#     search_fields = [
#         'title',
#     ]
#     pass
#
#
# class MySelect2MultipleWidget(ModelSelect2MultipleWidget):
#     queryset = Question.objects.all()
#     model = Question
#     dependent_fields = {
#         'test': 'test'
#     }
#     search_fields = [
#         'text',
#     ]
#
#
# class TaskForm(forms.ModelForm):
#
#     class Meta:
#         model = Task
#         fields = ('course', 'title', 'description', 'date_start', 'date_end', 'test', 'questions')
#         widgets = {
#             'test': MySelect2Widget,
#             'questions': MySelect2MultipleWidget
#         }
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # print(self.request)
#         print(list(self.fields['test'].queryset))
#         print(list(self.fields['questions'].queryset))
#         test = Test.objects.get(id=2)
#         self.fields['questions'].queryset = test.questions.all()

# class TaskForm(forms.Form):
#
#     test = forms.ModelChoiceField(
#         queryset=Test.objects.all(),
#         widget=ModelSelect2Widget(
#             model=Test,
#         )
#     )
#
#     questions = forms.ModelMultipleChoiceField(
#         queryset=Question.objects.all(),
#         widget=ModelSelect2MultipleWidget(
#             model=Question,
#             dependent_fields={'test': 'test'},
#             max_results=100
#         )
#     )
