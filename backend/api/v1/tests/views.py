from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from backend.tests.models import (
    TestCategory,
    Test,
    Question,
    PossibleAnswer,
    AnswersCounter
)
from .serializers import (
    TestCategorySerializer,
    TestSerializer,
    QuestionSerializer,
    PossibleAnswerSerializer
)

from backend.courses.models import RealizationTask
from backend.utils.api import BlankGetAPIView


class AllCategories(BlankGetAPIView):
    """
    Вывод всех категорий,
    параметров нет
    """
    permission_classes = [permissions.IsAuthenticated]
    model = TestCategory
    serializer = TestCategorySerializer


class TestsInCategory(BlankGetAPIView):
    """
    Вывод тестов в отдельной категории,
    параметр: pk, значение: id категории, тесты которой нужны
    """
    permission_classes = [permissions.IsAuthenticated]
    model = Test
    serializer = TestSerializer
    filter_name = 'category_id'


class QuestionsInTest(BlankGetAPIView):
    """
    Вывод вопросов в отдельном тесте,
    параметр: pk, значение: id теста, вопросы которого нужны
    """
    permission_classes = [permissions.IsAuthenticated]
    model = Question
    serializer = QuestionSerializer
    filter_name = 'test_id'
    order_params = 'id'


class AnswersInQuestion(BlankGetAPIView):
    """
    Вывод вариантов ответа к вопросу,
    параметр: pk, значение: id вопроса, ответы которого нужны
    """
    permission_classes = [permissions.IsAuthenticated]
    model = PossibleAnswer
    serializer = PossibleAnswerSerializer
    filter_name = 'question_id'
    order_params = '-id'


class CompleteQuestion(APIView):
    """Вывод результатов теста и его прохождение"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        pks = request.data.getlist('pks[]', None)
        if not pks:
            return Response('Не указано "pks"', status=400)
        # pks = pks.split()
        # pks = str(pks)
        # print(type(pks))
        # print([str(x) for x in pks])
        variants = PossibleAnswer.objects.filter(id__in=pks)
        right_variants = variants.filter(is_right=True)

        # Количество верных вариантов
        right_count = right_variants.count()

        # Наличие привязанного таска
        task_exists = variants.first().question.test.tasks.exists()

        # Общее количество вопросов в тесте
        total_questions = variants.first().question.test.questions.count()

        # Проверка на совпадение количества правильных ответов
        # и общего количества вопросов
        success = right_count >= total_questions

        if success:
            # Получаем RealizationTask текущего юзера и отмечаем его пройденным
            realization = self.get_realization(request.user, variants.first())
            if realization is not None:
                realization.success = True
                realization.save()

        return Response({
            'task': {
                'exists': task_exists,
                'success': success if task_exists else None
            },
            'total': total_questions,
            'right': right_count
        })

    # def post(self, request):
    #     """Прохождение теста"""
    #     pk = request.data.get('pk')  # id варианта ответа
    #
    #     try:
    #         variant = PossibleAnswer.objects.get(id=pk)
    #     except ObjectDoesNotExist:
    #         return Response('Нет такого варианта', status=404)
    #
    #     counter = self.get_counter(request.user, variant.question.test.id)
    #
    #     if variant.is_right:
    #         counter.counter += 1
    #         counter.save()
    #
    #     if counter.counter >= counter.questions_count:
    #         realization = self.get_realization(request.user, variant)
    #
    #         if realization is None:
    #             counter.delete()
    #             return Response('Не жульничай', status=400)
    #
    #         realization.success = True
    #         realization.save()
    #
    #     return Response(status=200)

    def get(self, request):
        """Вывод результатов"""
        pk = request.GET.get('pk')  # id теста
        counter = self.get_counter(request.user, pk)
        return Response({'total': counter.questions_count,
                         'right': counter.counter})

    @staticmethod
    def get_counter(user, pk):
        """Получение счетчика правильных ответов"""
        test = Test.objects.get(id=pk)
        try:
            counter = AnswersCounter.objects.get(user=user, test=test)
        except ObjectDoesNotExist:
            counter = AnswersCounter.objects.create(user=user, test=test)
        # counter = AnswersCounter.objects.get_or_create(user=user, test=test)
        return counter

    @staticmethod
    def get_realization(user, variant):
        """Получение модели выполнения задания"""
        try:
            realization = RealizationTask.objects.get(
                student=user,
                task__test__questions__answers__id=variant.id
            )
            return realization
        except ObjectDoesNotExist:
            return None
