# Django Rest Framework Validation Order Issue

This example project illustrates a validation order issue in the Django Rest Framework. If you have custom validation in 
a serializer that depends on other fields, if the field validation fails then the response doesn't show the custom
validation errors. This ends up being a bad user experience because the user can end up fixing the field error and then
when post another request they can end up getting errors thrown in the custom validation.

If you run the tests in this example project you'll see that currently the test `TestPizzaSerializer.test_invalid_data`
fails because of the way that Django Rest Framework calls it's validation.

In contrast if you run the test `TestPizzaForm.test_invalid_data` which is testing identical validation logic but in a
Django ModelForm, it passes as you would expect it to, showing all the errors.
 
## Install

    $ cd ~/Sites  # Or directory where you keep projects
    $ git clone https://github.com/epicserve/drf-validation-issue.git
    $ cd drf-validation-issue
    $ mkvirtualenv drf-validation-issue
    $ workon drf-validation-issue
    $ echo `pwd` >  $VIRTUAL_ENV/.project
    $ pip install poetry
    $ poetry install
    $ ./manage.py migrate \
      && ./manage.py load_toppings \
      && ./manage.py createsuperuser

# Run Tests

    $ pytest
