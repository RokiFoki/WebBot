from webbot import WebBot


with WebBot() as wb:

    response = wb.connect("www.google.com/")
    site = wb.get_content()

    wb.search("Linkedin Roko Krstulovic", title="Traži")

    print(site)


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