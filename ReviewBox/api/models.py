from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.

class Movies(models.Model):
    title=models.CharField(max_length=200)
    genre=models.CharField(max_length=200)
    language=models.CharField(max_length=200)
    year=models.PositiveIntegerField()
    runtime=models.TimeField()
    poster_image=models.ImageField(upload_to="images",default="default.jpg",null=True,blank=True)
    director=models.CharField(max_length=200)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    
    @property
    def reviews(self):
        return self.moviereview.all()

    @property
    def avg_rating(self):
        reviews=self.moviereview.all()
        if reviews:
            review_count=reviews.count()
            total_rating=sum([r.rating for r in reviews])
            avg=total_rating/review_count
            return avg
        else:
            return 0


    def __str__(self):
        return self.title
    
class Reviews(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="userreview")
    movie=models.ForeignKey(Movies,on_delete=models.CASCADE,related_name="moviereview")
    comment=models.CharField(max_length=200)
    rating=models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(10)])
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)   

    def __str__(self):
        return self.comment
    
    class Meta:
        unique_together=("user","movie")


