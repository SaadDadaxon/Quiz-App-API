from django.db import models
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from account.models import Account
from .models import Category, Question, Answers, Result, Token
from .serializer import CategorySerializer, QuestionGETSerializer, ResultSerializer
from django.db.models import Count, Avg
from account.serializer import MyAccountResultSerializer
from django.db.models.functions import TruncMonth, TruncWeek, TruncDay


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# class QuestionList(APIView):
#
#     def post(self, *args, **kwargs):
#         author_id = self.request.user.id
#         category_id = self.kwargs.get('category_id')
#         result = Result.objects.create(category_id=category_id, author_id=author_id)
#         questions = Question.objects.filter(category_id=category_id).order_by('?')[:5]
#         for question in questions:
#             result.questions.add(question)
#         result.save()
#         serializer = ResultSerializer(result)
#         return Response({'data': serializer.data})


class QuestionList(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionGETSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        if qs:
            qs = qs.filter(category_id=category_id).order_by('?')[:5]
            return qs
        return []


class AnswerStudent(APIView):

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'category_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='ID of the category.'
                ),
                'questions': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'question_id': openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description='ID of the question.'
                            ),
                            'answers_id': openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description='ID of the answer.'
                            ),
                        }
                    )
                )
            },
            required=['category_id', 'questions'],
            example={
                'category_id': 1,
                'questions': [
                    {
                        'question_id': 1,
                        'answers_id': 1
                    },
                    {
                        'question_id': 4,
                        'answers_id': 12
                    },
                    {
                        'question_id': 6,
                        'answers_id': 16
                    }
                ]
            }
        )
    )
    def post(self, request, *args, **kwargs):
        statistic = []
        j = 0
        author_id = request.user.id
        category_id = request.data.get('category_id')
        questions = request.data.get('questions')
        result = Result.objects.create(category_id=category_id, author_id=author_id)
        questions_ids = [i.id for i in Question.objects.filter(category_id=category_id).order_by('?')[:5]]
        count = 0
        wrong = 0
        question_sort = []
        question_count = len(questions_ids)
        for i in questions:
            question_id = int(i.get('question_id'))
            answer_id = int(i.get('answers_id'))
            answers_ids = [i.id for i in Answers.objects.filter(question_id=question_id)]
            if answer_id not in answers_ids:
                return Response({'message': f'Bunday javob mavjud emas!'})
            if question_id not in questions_ids:
                return Response({'message': 'Bunday savol mavjud emas!'})
            if question_id in question_sort:
                return Response({'message': "1 ta savolga 2 marta javob berib bo'lmaydi!"})
            try:
                question = Question.objects.get(id=question_id)
                answer = Answers.objects.get(id=answer_id)
            except (Question.DoesNotExist, Answers.DoesNotExist):
                continue
            statistic.append({
                'Question': QuestionGETSerializer(question).data,
                'Answer': answer.id,
            })
            question_answer_true = Question.objects.filter(answers__is_true=True, category_id=category_id,
                                                           id=question_id, answers=answer)
            if question_answer_true:
                count += 1
                statistic[j]['Student answer'] = True
            else:
                wrong += 1
                statistic[j]['Student answer'] = False
            result.questions.add(question)
            question_sort.append(question_id)
            j += 1
        result.result = count / question_count * 100
        result.save()
        serializer_result = ResultSerializer(result).data
        response_data = {
            'result': serializer_result,
            'statistics': statistic
        }

        return Response(response_data)


class AnswerStudentUrls(APIView):

    def post(self, request, *args, **kwargs):
        author_id = request.user.id
        category_id = self.kwargs.get('category_id')
        questions_id = self.kwargs.get('questions_id')
        answers_id = self.kwargs.get('answers_id')
        count = 0
        result = Result.objects.create(category_id=category_id, author_id=author_id)
        answer = Answers.objects.get(id=answers_id)
        question_true = Question.objects.filter(category_id=category_id, id=questions_id, answers=answer,
                                                answers__is_true=True)
        if question_true:
            count += 1
        else:
            return Response({'You url was wrong'})
        result.questions.add(questions_id)
        result.result = count
        result.save()
        return Response("Result was saved")


class MonthStatic(APIView):
    def get(self, request):
        month = []
        total_results = []
        average = []
        results = Result.objects.annotate(month=TruncMonth('create_date'))
        monthly_statistics = results.values('month').annotate(total_results=Count('id'), avg_result=Avg('result'))
        for stat in monthly_statistics:
            month = stat['month']
            average = stat['avg_result']
            total_results = stat['total_results']

        return Response({"Month": month, "average": round(average), "Total Results": total_results})


class WeekStatic(APIView):
    def get(self, request):
        week = []
        average = []
        count = []

        results = Result.objects.annotate(week=TruncWeek('create_date')).values('week').annotate(
            avg_result=Avg('result'),
            count_result=Count('result')
        )

        for result in results:
            week = result['week']
            average = result['avg_result']
            count = result['count_result']

        return Response({"Week": week, "Average": average, "Count": count})


class ResultList(APIView):
    def get(self, *args, **kwargs):
        categories = Category.objects.all()
        cate_result = []
        for category in categories:
            average = Result.calculate_average_result(category)
            if average is not None:
                round_average = round(average, 2)
                cate_result.append({'category': category.title, 'average': round_average})
            cate_result.append({'category': category.title, 'average': average})
        return Response({'data': cate_result})


class ResultListAccount(APIView):
    def get(self, *args, **kwargs):
        accounts = Account.objects.all()
        data = []
        for author in accounts:
            account_result = Result.account_average_result(author)
            account_detail = MyAccountResultSerializer(author).data
            data.append({
                "account_result": round(account_result),
                "account_detail": account_detail,
            })
        return Response(data)


class DayStatic(APIView):
    def get(self, request, *args, **kwargs):
        day = []
        total_results = []
        average = []
        results = Result.objects.annotate(day=TruncDay('create_date'))
        daily_statistics = results.values('day').annotate(total_results=Count('id'), avg_result=Avg('result'))
        for stat in daily_statistics:
            day = stat['day']
            average = stat['avg_result']
            total_results = stat['total_results']
        return Response({"Day": day, "average": round(average), "Total Results": total_results})


class CategoryStatisticsAPIView(APIView):
    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not start_date or not end_date:
            return Response({'message': 'start_date and end_date parameters are required'}, status=400)

        try:
            start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
        except (TypeError, ValueError):
            return Response({'message': 'start_date and end_date must be in the format YYYY-MM-DD'}, status=400)

        category_stats = Result.objects.filter(create_date__range=(start_date, end_date)).values_list('category')\
            .annotate(attempts=models.Count('id'), total_result=models.Avg('result'))\
            .values('category__title', 'author__email', 'attempts', 'total_result')

        statistics = []

        for category in category_stats:
            category_info = {
                'category': category['category__title'],
                'author': category["author__email"],
                'attempts': category['attempts'],
                'total_result': category['total_result']
            }
            statistics.append(category_info)

        return Response(statistics)
