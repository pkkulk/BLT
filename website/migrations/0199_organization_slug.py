# Generated by Django 5.1.6 on 2025-02-16 01:18

from django.db import migrations, models
from django.utils.text import slugify


def generate_unique_slugs(apps, schema_editor):
    Organization = apps.get_model("website", "Organization")
    # Get existing slugs
    used_slugs = set(Organization.objects.exclude(slug__isnull=True).values_list("slug", flat=True))

    # Process all organizations without a slug (null or empty)
    for org in Organization.objects.filter(slug__isnull=True):
        base_slug = slugify(org.name)
        if not base_slug:
            base_slug = f"org-{org.id}"

        slug = base_slug
        counter = 1

        # Keep incrementing counter until we find a unique slug
        while slug in used_slugs:
            slug = f"{base_slug}-{counter}"
            counter += 1

        used_slugs.add(slug)
        org.slug = slug
        org.save()


def reverse_slug_generation(apps, schema_editor):
    Organization = apps.get_model("website", "Organization")
    Organization.objects.all().update(slug=None)


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0198_alter_githubissue_issue_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="organization",
            name="slug",
            field=models.SlugField(null=True, blank=True, max_length=255),
        ),
        migrations.RunPython(
            generate_unique_slugs,
            reverse_slug_generation,
            elidable=False,
        ),
        migrations.AlterField(
            model_name="organization",
            name="slug",
            field=models.SlugField(unique=True, max_length=255, null=False, blank=False),
        ),
    ]
