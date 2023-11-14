from django.contrib.auth.models import AbstractUser
from django.db import models


# This code extends Django's default user model to create a custom user model named User.
# It doesn't add any additional fields or methods but allows for the potential addition of custom fields
# or behaviors in the future if needed.

# User class: Represents a user in the application. By inheriting from AbstractUser, this model includes fields
# and methods provided by Django's default user model, such as username, password, email, first name, last name, etc.
class User(AbstractUser):
    # pass: The pass statement is used to indicate that the class body is intentionally left empty.
    # In this case, it means that the User model does not include any additional fields or methods
    # beyond what is provided by AbstractUser.
    pass


# The Category model is designed to store categories for auction listings, and the __str__ method ensures
# that when you print or display a Category instance, it shows the category name for better readability.
# in a simple way : The Category model represents different categories for listings.
class Category(models.Model):
    # name (CharField): CharField for the category name. Represents a string attribute for the name of the category.
    # It is limited to a maximum length of 35 characters.
    name = models.CharField(max_length=35)

    # __str__ method: Overrides the default string representation method for instances of the Category model.
    # It specifies that when an instance of Category is converted to a string (for display purposes,
    # like in the Django admin), it should return the value of the name attribute.
    def __str__(self):
        return self.name


# The Listing model captures essential information about an auction listing, including details like title,
# description, bid amounts, status, category, creator, and creation timestamp.
# In simply way: Listing Model: Represents an auction listing.
class Listing(models.Model):
    # Stores a string with a maximum length of 60 characters, representing the title of the listing.
    title = models.CharField(max_length=25)
    # description (TextField): Stores a longer text description for the listing.
    description = models.TextField(max_length=500)
    # Represents the initial bid amount for the listing.
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    # Represents the current highest bid amount for the listing, with a default value of 0.00.
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # is_active (BooleanField): Indicates whether the listing is active or not, with a default value of True.
    is_active = models.BooleanField(default=True)
    # category (ForeignKey to Category model): Establishes a relationship with the Category model using a foreign key.
    # Each listing belongs to a specific category.
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='listings')
    # creator (ForeignKey to User model): Establishes a relationship with the User model using a foreign key.
    # Represents the user who created the listing.
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    # created_at (DateTimeField): Records the timestamp when the listing is created, automatically set to the current
    # date and time.
    created_at = models.DateTimeField(auto_now_add=True)
    # I added a new field named url to the Listing model. The models.URLField is used for storing URLs.
    # I set null=True and blank=True to allow for cases where the URL may not be provided.
    url = models.URLField(max_length=200, null=True, blank=True)
    # the model has a __str__ method that returns the title of the listing as its string representation.
    # This is useful for human-readable display in the Django admin interface and other contexts.A field for images

    def __str__(self):
        return self.title


# The Bid model captures information about a bid in an auction, including the associated listing,
# the user who placed the bid, the bid amount, and the timestamp of when the bid was created.
class Bid(models.Model):
    # listing (ForeignKey to Listing model): Establishes a relationship with the Listing model using a foreign key.
    # Each bid is associated with a specific auction listing.
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    # bidder (ForeignKey to User model): Establishes a relationship with the User model using a foreign key. Represents
    # the user who placed the bid.
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    # Represents the amount of the bid, stored as a decimal number with up to 10 digits in total and 2 decimal places.
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Records the timestamp when the bid is created, automatically set to the current date and time.
    created_at = models.DateTimeField(auto_now_add=True)


# The Comment model is designed to capture information about comments made on auction listings.
# It includes the associated listing, the user who posted the comment, the textual content of the comment,
# and the timestamp of when the comment was created.
class Comment(models.Model):
    # listing (ForeignKey to Listing model): Establishes a relationship with the Listing model using a foreign key.
    # Each comment is associated with a specific auction listing.
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    # commenter (ForeignKey to User model): Establishes a relationship with the User model using a foreign key.
    # Represents the user who posted the comment.
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    # content (TextField): Stores the textual content of the comment, allowing for longer text entries.
    content = models.TextField(max_length=300)
    # created_at (DateTimeField): Records the timestamp when the comment is created, automatically set to
    # the current date and time.
    created_at = models.DateTimeField(auto_now_add=True)

# ============================================


class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    listings = models.ManyToManyField('Listing')
