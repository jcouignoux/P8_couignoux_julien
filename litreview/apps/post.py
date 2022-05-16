from apps.models import Ticket, Review

from itertools import chain


def get_all_posts():
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()
    posts_list = sorted(
        chain(tickets, reviews),
        key=lambda post: post.time_created, reverse=True)
    return posts_list
