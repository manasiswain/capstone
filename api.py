from requests_html import HTMLSession


if __name__ == '__main__':
    session = HTMLSession()
    url = 'https://www.google.pl/search?q=python&source=lnms&tbm=isch&sa=X&ved=0ahUKEwif6Zq7i8vaAhVMLVAKHUDkDa4Q_AUICigB&biw=1280&bih=681'
    r = session.get(url)
    r.html.render()
    first_image = r.html.find('.rg_ic.rg_i', first=True)
    link = first_image.attrs['src']