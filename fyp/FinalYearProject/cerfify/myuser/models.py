
from djongo import models

from django.contrib.auth.models import AbstractUser

from submission.models import Submission



class MyUser(AbstractUser):
    # This is is to store the date of birth
    date_of_birth=models.DateField(null=True,blank=True)

    #Based on the work done a person is provided a rank
    rank=models.IntegerField(default=1)

    # This is an array of submissions. These are all the submissions by a Specific user.
    submissions = models.ArrayField(model_container=Submission,default=[])

    # This is what counts a person's score
    score=models.IntegerField(default=0)

    def increment_score(self,project_level,rank) :
        if(rank == 0 or rank >3 ):
            return
        threshold = self.get_threshold()
        self.score += (4-rank) * project_level
        if(self.score > threshold) :
            self.rank += 1

    def get_threshold(self):
        threshold = (2 ** (self.rank-1) )* 10
        return threshold
