from bs4 import BeautifulSoup
def extract_table(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [col.text.strip() for col in cols]
        data.append(cols)
    return data
  
  
html = """
<!DOCTYPE html>
<html>
<head>
    <!-- 省略其他部分 -->
</head>
<body>
    <h1>护肤品成分表</h1>

    <table>
        <!-- 表格的结构 -->
    </table>

</body>
</html>
"""

table_data = extract_table(html)
for row in table_data:
    print(row)
  
