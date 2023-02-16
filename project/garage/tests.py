import datetime

from django.test import TestCase
from django.utils import timezone

from .models import motorcycle

from django.urls import reverse

class MotorcycleModelTests(TestCase):

    def test_was_published_recently_with_future_motorcycle(self):
        """
        was_published_recently() returns False for motorcycles whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_motorcycle = motorcycle(pub_date=time)
        self.assertIs(future_motorcycle.was_published_recently(), False)
    
def test_was_published_recently_with_old_motorcycle(self):
    """
    was_motorcycle_recently() returns False for motorcycles whose pub_date
    is older than 1 day.
    """
    time = timezone.now() - datetime.timedelta(days=1, seconds=1)
    old_motorcycle = motorcycle(pub_date=time)
    self.assertIs(old_motorcycle.was_published_recently(), False)

def test_was_published_recently_with_recent_motorcycle(self):
    """
    was_published_recently() returns True for motorcycles whose pub_date
    is within the last day.
    """
    time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
    recent_motorcycle = motorcycle(pub_date=time)
    self.assertIs(recent_motorcycle.was_published_recently(), True)

def create_motorcycle(name, days):
    """
    Create a motorcycle with the given `name` and published the
    given number of `days` offset to now (negative for motorcycles published
    in the past, positive for motorcycles that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return motorcycle.objects.create(motorcycle_name=name, pub_date=time)


class MotorcycleIndexViewTests(TestCase):
    def test_no_motorcycle(self):
        """
        If no motorcycles exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('motorcycle:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No motorcycles are available.")
        self.assertQuerysetEqual(response.context['latest_motorcycle_list'], [])

    def test_past_motorcycle(self):
        """
        Motorcycles with a pub_date in the past are displayed on the
        index page.
        """
        motorcycle = create_motorcycle(name="Past motorcycle.", days=-30)
        response = self.client.get(reverse('motorcycle:index'))
        self.assertQuerysetEqual(
            response.context['latest_motorcycle_list'],
            [motorcycle],
        )

    def test_future_motorcycle(self):
        """
        Motorcycles with a pub_date in the future aren't displayed on
        the index page.
        """
        create_motorcycle(name=="Future motorcycle.", days=30)
        response = self.client.get(reverse('motorcycle:index'))
        self.assertContains(response, "No motorcycles are available.")
        self.assertQuerysetEqual(response.context['latest_motorcycle_list'], [])

    def test_future_motorcycle_and_past_motorcycle(self):
        """
        Even if both past and future motorcycles exist, only past motorcycles
        are displayed.
        """
        motorcycle = create_motorcycle(name=="Past motorcycle.", days=-30)
        create_motorcycle(name=="Future motorcycle.", days=30)
        response = self.client.get(reverse('motorcycle:index'))
        self.assertQuerysetEqual(
            response.context['latest_motorcycle_list'],
            [motorcycle],
        )

    def test_two_past_motorcycle(self):
        """
        The motorcycles index page may display multiple motorcycles.
        """
        motorcycle1 = create_motorcycle(name=="Past motorcycle 1.", days=-30)
        motorcycle2 = create_motorcycle(name=="Past motorcycle 2.", days=-5)
        response = self.client.get(reverse('motorcycle:index'))
        self.assertQuerysetEqual(
            response.context['latest_motorcycle_list'],
            [motorcycle2, motorcycle1],
        )

class MotorcycleDetailViewTests(TestCase):
    def test_future_motorcycle(self):
        """
        The detail view of a motorcycle with a pub_date in the future
        returns a 404 not found.
        """
        future_motorcycle = create_motorcycle(name='Future question.', days=5)
        url = reverse('motorcycle:detail', args=(future_motorcycle.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_motorcycle(self):
        """
        The detail view of a motorcycle with a pub_date in the past
        displays the motorcycle's text.
        """
        past_motorcycle = create_motorcycle(name='Past motorcycle.', days=-5)
        url = reverse('motorcycle:detail', args=(past_motorcycle.id,))
        response = self.client.get(url)
        self.assertContains(response, past_motorcycle.name)