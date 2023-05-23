from django.db import models


class Submission(models.Model):


    class Meta:
    # This means that submissions is not created in the database
        abstract = True

    # The Submitter information is given as username
    submitter = models.CharField(max_length=200)

    #The files given by the submitter
    files = models.URLField()

    # The Date and time the submission was made
    dateTimeField = models.DateTimeField()

    # The project to which the submission was made
    project = models.IntegerField()

    # The rank of the submission given by the creator of the project
    rank = models.IntegerField()

