from django.db.models.signals import post_save
from django.dispatch import receiver, Signal

# from bboard.models import Bb
#
#
# @receiver(post_save)
# def post_save_dispatcher(sender, **kwargs):
#     snd = sender
#     instance = kwargs['instance']
#     if type(instance) is Bb:
#         print(snd, '\n', instance)
#     else:
#         print('С И Г Н А Л')
#
#
# @receiver(post_save, sender=Bb)
# def add_bb_dispatcher_1(sender, **kwargs):
#     if sender['created']:
#         print("С О З Д А Л", kwargs['instance'].rubric.name)
#     else:
#         print('И З М Е Н И Л')


def add_bb_dispatcher_2(sender, **kwargs):
    # print("add_bb_dispatcher_2")
    print(f'Объявление в рубрике {kwargs["instance"].rubric.name} с ценой {kwargs["instance"].price} создано')


# post_save.connect(post_save_dispatcher)
# post_save.connect(post_save_dispatcher, sender=Bb)
# post_save.connect(post_save_dispatcher, dispatch_uid='post_save_dispatcher_1')
# post_save.connect(post_save_dispatcher, dispatch_uid='post_save_dispatcher_2')
#
# post_save.disconnect(receiver=post_save_dispatcher)
# post_save.disconnect(receiver=post_save_dispatcher, sender=Bb)
# post_save.disconnect(dispatch_uid='post_save_dispatcher_1')

add_bb = Signal()

add_bb.connect(add_bb_dispatcher_2)
