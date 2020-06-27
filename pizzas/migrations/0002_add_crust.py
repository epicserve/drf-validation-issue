# Generated by Django 3.0.7 on 2020-06-27 18:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pizzas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crust',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='pizza',
            name='crust',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, to='pizzas.Crust'),
            preserve_default=False,
        ),
    ]