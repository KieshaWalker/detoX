#!/usr/bin/env python
"""
Email Configuration Test Script for detoX
Run this to verify your email settings are working correctly.
"""

import os
import sys
from urllib import response
import requests
import django
import requests


def send_simple_message():
  	return requests.post(
  		"https://api.mailgun.net/v3/sandboxa999fa14610447bd8b1cfe800e270b15.mailgun.org/messages",
  		auth=("api", os.getenv('API_KEY', 'API_KEY')),
  		data={"from": "Mailgun Sandbox <postmaster@sandboxa999fa14610447bd8b1cfe800e270b15.mailgun.org>",
			"to": "k walker <llcwalkerk@gmail.com>",
  			"subject": "Hello k walker",
  			"text": "Congratulations k walker, you just sent an email with Mailgun! You are truly awesome!"})
print("✅ Email sent successfully using Mailgun API")

if __name__ == '__main__':
    send_simple_message()