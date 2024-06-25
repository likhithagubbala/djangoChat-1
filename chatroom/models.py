from django.db import models

class Room(models.Model):
    room_name = models.CharField(max_length=50)

    def __str__(self):
        return self.room_name 

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    author = models.CharField(max_length=50)  # Changed from 'sender' to 'author'
    content = models.TextField()  # Changed from 'message' to 'content'
    time_stamp = models.DateTimeField(auto_now_add=True)  # Add a timestamp field

    def __str__(self):
        return f"{str(self.room)} - {self.author}"
