from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    visited_exhibits = models.ManyToManyField('Exhibit', related_name='visitors', blank=True)
    total_museum_points = models.IntegerField(default=0)
    room_points = models.ManyToManyField('Room', through='UserRoomPoints', blank=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    
    def calculate_total_museum_points(self):
        total_points = sum(exhibit.points for exhibit in self.visited_exhibits.all())
        self.total_museum_points = total_points
        self.save()

class Exhibit(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    points = models.IntegerField(default=0)
    room = models.ForeignKey('Room', on_delete=models.CASCADE, to_field='room_number', default='0')

        
    def __str__(self):
        return self.name

class Room(models.Model):
    room_number = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    max_points = models.IntegerField(default=0)


    def __str__(self):
        return self.name

    def calculate_max_points(self):
        total_max_points = sum(exhibit.points for exhibit in self.exhibit_set.all())
        self.max_points = total_max_points
        self.save()

class UserRoomPoints(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exhibit = models.ForeignKey(Exhibit, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)   

    def __str__(self):
        return f"Comment by {self.user.username} on {self.exhibit.name}"
