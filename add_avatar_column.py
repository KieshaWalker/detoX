#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'detoX.settings')
django.setup()

from django.db import connection

cursor = connection.cursor()
try:
    cursor.execute("ALTER TABLE \"X_app_userprofile\" ADD COLUMN IF NOT EXISTS avatar varchar(100);")
    print("✅ Avatar column added successfully")
except Exception as e:
    print(f"❌ Error adding avatar column: {e}")