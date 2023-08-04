from django.db import models


class Trait(models.Model):
    name = models.CharField(max_length=20, unique=True)
    # pet = models.ManyToManyField("pets.Pet")

    def __repr__(self):
        return f"<[{self.pk}] {self.name}>"
