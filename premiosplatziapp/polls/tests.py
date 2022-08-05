import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls.base import reverse

from .models import Question


#Normalmente se testean models o views
class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """was_published_recently returns False
         for question whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="Quien es el mejor Course Director",pub_date = time)
        self.assertIs(future_question.was_published_recently(),False)


def create_question(question_text,days):
    """
    Create a question whit the given "question_text", and published
    the given number of days offset to now(negative for question in the past,
    positive for question tha have yet to be published)
    """
    time= timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,pub_date=time)

class QuestionIndexViewTest(TestCase):
    
    def test_no_question(self):
        """if no question exist, an appropiate message is displayed"""
        response=self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"],[])    

    def test_future_question(self):
        """
        Question whit a pub_date in the future aren't display on the index page
          """
        create_question("Future question",days=30)
        response=self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")  
        self.assertQuerysetEqual(response.context["latest_question_list"],[])

    def test_past_question(self):        
        """
        Question with a pub_date in the past are displayed on the index page
        """
        question = create_question("Past question",days=-10)
        response=self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],[question])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questios exist, only past question are displayed
        """
        past_question = create_question(question_text="Past question",days=-30)
        future_question = create_question(question_text="Future question",days=30)
        response= self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],[past_question])


    def test_two_past_question(self):
        """
        The questions index page my display multiple question.

        """
        past_question1 = create_question(question_text="Past question 1",days=-30)
        past_question2 = create_question(question_text="Past question 2",days=-50)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],[past_question1,past_question2])



