from webbot import WebBot
import re


with WebBot() as wb:

    response = wb.connect("www.google.com/")

    wb.search("Roko Krstulović", args={"title": "Traži"}, submit=True)
    wb.wait(tag="a")
    wb.click(string=re.compile("Professional Profile"), driver=True)
    wb.wait(tag="a", args={"text": "Sign in"})
    wb.click(string="Sign in", driver=True)
    wb.wait(10)
