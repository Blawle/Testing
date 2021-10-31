from bs4 import BeautifulSoup
html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>First HTML Page</title>
</head>
<body>
  <div id="first">
    <h3 data-example="yes">hi</h3>
    <p>more text.</p>
  </div>
  <ol>
    <li class="special super-special">This list item is special.</li>
    <li>This list item is not special.</li>
    <li class="special">This list item is also special.</li>
    </ol>
  <div data-example="yes">bye</div>
</body>
</html>
"""

soup = BeautifulSoup(html, "html.parser")
data1 = soup.body.contents[1].next_sibling.next_sibling
data2 = soup.find(class_="super-special").parent.parent
data3 = soup.find(id="first").find_next_sibling().find_next_sibling()
data4 = soup.select("[data-example]")[1].find_previous_sibling()
data5 = soup.find(class_="super-special").find_next_sibling(class_="special")
data = soup.find("h3").find_parent("html")

print(data)
print(data1)
print(data2)
print(data3)
print(data4)
print(data5)