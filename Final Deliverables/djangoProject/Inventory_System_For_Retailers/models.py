from django.db import models


class Stock(models.Model):
    Product_Name = models.CharField(max_length=100)
    Recently_Updated = models.DateTimeField('date Updated')
    Date_Added = models.DateTimeField('date Added')
    No_of_stocks = models.IntegerField(default=0)
    Price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0)
    Tax = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0)

    def __str__(self) -> str:
        return self.Product_Name + " - No of Stocks " + str(self.No_of_stocks)
