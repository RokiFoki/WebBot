from webbot import WebBot
import re


with WebBot() as wb:

    response = wb.connect("www.google.com/")

    wb.search("Roko Krstulović", title="Traži")
    wb.click(string=re.compile("Professional Profile"), driver=True)
    content = wb.get_content()
    wb.wait(10)
    print(content)



"""
wb = WebBot()

wb.connect("www.google.com")
site = wb.get_content()
print(site)

wb.input(title="search", text="Linkedin Roko Krstulovic")
wb.click(string="Google Search")

site=wb.get_content()
print(site)

"""