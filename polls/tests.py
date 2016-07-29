import datetime 

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse


from .models import Question
# Create your tests here.

def create_question(question_text, days):
    """
    Creates a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionMethodTests(TestCase):

	
	def test_was_published_recently_with_future_question(self):
		time = timezone.now()+datetime.timedelta(days=30)
		#Create a question that was published in the future.
		future_question = Question(pub_date = time)
		self.assertEqual(future_question.was_published_recently(),False)

	def test_was_published_recently_with_old_question(self):
		old_time = timezone.now()-datetime.timedelta(days=30)

		old_question = Question(pub_date=old_time)
		self.assertEqual(old_question.was_published_recently(),False)

	def test_was_published_recently_with_recent_question(self):
		time = timezone.now()-datetime.timedelta(hours=1)
		recent_question= Question(pub_date=time)

		self.assertEqual(recent_question.was_published_recently(),True)

	
class QuestionViewTests(TestCase):
	def test_index_view_with_no_questions(self):
		"""
		If no questions exist, an appropriate message should be displayed.
		"""
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response, "No polls are available.")
		self.assertQuerysetEqual(response.context['latest_question_list'],[])

	def test_index_view_with_a_past_question(self):
		"""
		Questions with a pub_date in the past should be displayed on the
		index page.
		"""
		create_question(question_text="Past question.",days=-30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			['<Question: Past question.>']
		)

	def test_index_view_with_a_future_question(self):
		"""
		Questions with a pub_date in the future should not be displayed on
		the index page.
		"""
		create_question(question_text="Future question.", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertContains(response, "No polls are available.")
		self.assertQuerysetEqual(response.context['latest_question_list'], [])

	def test_index_view_with_future_and_past_question(self):
		create_question(question_text="future question.",days=30)
		create_question(question_text="past question.",days=-30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],['<Question: past question.>']
		)

	def test_index_view_with_two_past_questions(self):
		create_question(question_text="past question1.",days=-30)
		create_question(question_text="past question2.",days=-30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			['<Question: past question2.>','<Question: past question1.>']
		)


		