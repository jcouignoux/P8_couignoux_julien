from apps.models import Ticket, Review

from itertools import chain


def get_all_posts(user):

    if user == 'all':
        tickets = Ticket.objects.all()
        reviews = Review.objects.all()
    else:
        tickets = Ticket.objects.filter(user=user)
        reviews = Review.objects.filter(user=user)

    posts_list = sorted(
        chain(tickets, reviews),
        key=lambda post: post.time_created, reverse=True)
    return posts_list
