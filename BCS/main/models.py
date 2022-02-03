from django.db import models


class Transaction(models.Model):
    trans_id = models.CharField('ID транзакции', max_length=255, default='null')
    trans_description = models.TextField('Описание', default='null', blank=True)

    def __str__(self):
        return self.trans_id
