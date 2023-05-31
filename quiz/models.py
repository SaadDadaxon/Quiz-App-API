from django.db import models, IntegrityError
from account.models import Account
from django.utils import timezone
from django.db.models import Avg, Max, Min, Sum, UniqueConstraint, Q


class Category(models.Model):
    title = models.CharField(max_length=228)

    def __str__(self):
        return self.title


class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    questions = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.questions


class Answers(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer = models.CharField(max_length=888)
    is_true = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['question'],
                condition=Q(is_true=True),
                name='unique_correct_option'
            )
        ]

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            raise IntegrityError('Only one option can be marked as correct for a question.')

    def __str__(self):
        return f"{self.question}'s answers"


class Result(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question)
    result = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.result}"

    @classmethod
    def calculate_average_result(cls, category):
        average_category = cls.objects.filter(category=category).aggregate(Avg('result'))['result__avg']
        return average_category

    @classmethod
    def account_average_result(cls, author):
        average_results_by_account = cls.objects.filter(author=author).aggregate(Avg('result'))['result__avg']
        return average_results_by_account

    # @staticmethod
    # def get_daily_statistics(category_id, start_date):
    #     end_date = start_date + timezone.timedelta(days=1)  # Kechasi kunni hisoblash
    #     results = Result.objects.filter(category_id=category_id, create_date__gte=start_date, create_date__lt=end_date)
    #     daily_statistics = {
    #         'category_id': category_id,
    #         'start_date': start_date,
    #         'end_date': end_date,
    #         'results': list(results.values('author_id', 'result'))  # Kerakli ma'lumotlarni olish
    #     }
    #     return daily_statistics


class Token(models.Model):
    token = models.CharField(max_length=100, unique=True)
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Qo'shimcha xususiyatlar va metodlar

    def __str__(self):
        return self.token
