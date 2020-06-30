from collections import OrderedDict
from collections.abc import Mapping

from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SkipField, empty, get_error_detail, set_value
from rest_framework.serializers import as_serializer_error
from rest_framework.settings import api_settings

from pizzas.models import Crust, Pizza, Topping, ToppingType


class PizzaSerializer(serializers.HyperlinkedModelSerializer):

    def to_internal_value(self, data):
        """
        Override rest_framework.serializers.Serializer.to_internal_value in order to returned errors and cleaned data
        """
        if not isinstance(data, Mapping):
            message = self.error_messages['invalid'].format(
                datatype=type(data).__name__
            )
            raise ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: [message]
            }, code='invalid')

        ret = OrderedDict()
        errors = OrderedDict()
        fields = self._writable_fields

        for field in fields:
            validate_method = getattr(self, 'validate_' + field.field_name, None)
            primitive_value = field.get_value(data)
            try:
                validated_value = field.run_validation(primitive_value)
                if validate_method is not None:
                    validated_value = validate_method(validated_value)
            except ValidationError as exc:
                errors[field.field_name] = exc.detail
            except DjangoValidationError as exc:
                errors[field.field_name] = get_error_detail(exc)
            except SkipField:
                pass
            else:
                set_value(ret, field.source_attrs, validated_value)

        return ret, errors

    def run_validation(self, data=empty):
        """
        Override the run_validation method found in rest_framework.serializers.Serializer.run_validation so that we can
        return all the errors at once instead of one at a time for a better user experience.
        """
        (is_empty_value, data) = self.validate_empty_values(data)
        if is_empty_value:
            return data

        cleaned_data, errors = self.to_internal_value(data)
        try:
            self.run_validators(cleaned_data)
            value = self.validate(cleaned_data)
            assert value is not None, '.validate() should return the validated data'
        except (ValidationError, DjangoValidationError) as exc:
            # Combine field level validation errors with custom validation errors
            combined_errors = OrderedDict()
            custom_validation_errors = as_serializer_error(exc)
            for field_name in self.fields:
                if field_name in errors:
                    combined_errors[field_name] = errors[field_name]
                if field_name in custom_validation_errors:
                    if field_name in combined_errors:
                        combined_errors[field_name].append(custom_validation_errors[field_name])
                    else:
                        combined_errors[field_name] = custom_validation_errors[field_name]
            raise ValidationError(combined_errors)

        # raise validation here if there are only field level validation errors
        if errors:
            raise ValidationError(errors)

        return value

    class Meta:
        model = Pizza
        fields = ('url', 'name', 'price', 'crust', 'toppings')

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price can't be less than zero.")
        return value

    def validate(self, data):

        # Require at least 1 sauce and cheese > 0
        sauce_num = 0
        cheese_num = 0
        for topping in data.get('toppings', []):
            if topping.type.slug == 'sauce':
                sauce_num += 1
            if topping.type.slug == 'cheese':
                cheese_num += 1

        topping_errors = []
        if sauce_num != 1:
            topping_errors.append("No sauce, please add some sauce.")

        if cheese_num < 1:
            topping_errors.append("No cheese, please add some cheese.")

        if topping_errors:
            raise serializers.ValidationError({'toppings': topping_errors})

        return data


class CrustSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Crust
        fields = ('name', )


class ToppingTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ToppingType
        fields = ('name', )


class ToppingSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Topping
        fields = ('name', 'type')
