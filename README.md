# Django Rest Framework Validation Order Issue

This example project illustrates a validation order issue in the Django Rest Framework. If you have custom validation in 
a serializer that depends on other fields, if the field validation fails then the response doesn't show the custom
validation errors. This ends up being a bad user experience because the user can end up fixing the field error and then
when the user posts another request they can end up getting errors thrown in the custom validation instead of being able
to see all the errors at once.

If you run the tests in this example project you'll see that currently the test `TestPizzaSerializer.test_invalid_data`
fails because of the way that Django Rest Framework calls it's validation.

In contrast if you run the test `TestPizzaForm.test_invalid_data` which is testing identical validation logic but in a
Django ModelForm, it passes as you would expect it to, showing all the errors.

If you checkout the branch `fix-validation` you can see that the tests all pass. The solution was to override two Django
Rest Framework methods in the Serializer class (`to_internal_value` and `run_validation`). The `to_internal_value` was
overwritten in order to not raise validation errors at this level and to also return cleaned data, instead we wait to
raise the Validation errors in the `run_validation` method so that they can all returned at once.
 
## Install

The following assumes you've already installed Python 3.8.3 and [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/).

    $ cd ~/Sites  # Or directory where you keep projects
    $ git clone https://github.com/epicserve/drf-validation-issue.git
    $ cd drf-validation-issue
    $ . ./bin/bootstrap.sh

## Run Tests

    $ pytest
