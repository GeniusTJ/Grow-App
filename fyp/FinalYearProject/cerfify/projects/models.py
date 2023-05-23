from djongo import models
from submission.models import Submission



class Project(models.Model):
    # This is the price the creator of the project is willing to give
    amount = models.DecimalField("Offered Price", max_digits=6, decimal_places=2)

    # The username of the creator of the project
    creator = models.CharField(max_length=200)

    # This is an array of submissions. The submissions contain the creator,thesubmitter and the files
    submissions = models.ArrayField(model_container=Submission ,default=[])

    # The date it needs to be submitted
    deadline = models.DateField()
    # #tags=models.ArrayField(model_container=models.CharField(max_length=40))

    # The Name of the project
    name = models.CharField(max_length=200)

    # A Description of the project
    description = models.CharField(max_length=5000)

    # The difficulty rank for the project
    ranked = models.BooleanField()

    # Date Posted

    date_posted = models.DateField()

    # Project Level
    level= models.IntegerField(default=1)
    # What happens when we type print(project)
    def __str__(self):
        return self.name
    # A Function to get the number of submissions made
    def get_no_of_submissions(self):
        return len(self.submissions)

