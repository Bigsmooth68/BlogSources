import requests, datefinder, re
from pathlib import Path
from bs4 import BeautifulSoup
from colorama import Fore, Style

root_url = 'https://www.dbi-services.com/blog/'
author_url = root_url + 'author/ols/'
dest_path = 'content\dbi-blogs\\'

def getBlogs(url,destination):
	maxPage = 0
	m = []
	html_text = requests.get(url).text
	soup = BeautifulSoup(html_text,'html.parser')

	for link in soup.find_all('a',href=True):
		lk = link.get('href')
		lkClass = link.get('class')
		if 'https://www.dbi-services.com/blog/' in lk:
			if 'text-decoration-none' in lkClass:
				title = link.h2.string.strip()
				sanitized_title = lk.replace(root_url,'').replace('/','')
				infos = (link.find('div',class_='infos')).text
				pubDate = next(datefinder.find_dates(infos))
				pubDateStr = str(pubDate)
				pubDateStr = pubDateStr.split()[0]

				path = Path( destination + sanitized_title + '.md')
				
				if not (path.is_file()):
					buildStr = '---\n'
					buildStr += f'title: "{ title }"\n'
					buildStr += f'date: { pubDateStr }\n'
					buildStr += 'tags: [""]\n'
					buildStr += f'dbiblogtitle: { sanitized_title }\n'
					buildStr += '---'
					path.write_text(buildStr)
					print(f'{sanitized_title} {Fore.GREEN}written{Fore.RESET}.')
				else:
					print(f'{sanitized_title} {Fore.RED}ignored{Fore.RESET}.')
			if 'page-link' in lkClass:
				m = re.findall('\/([0-9]+)\/',lk)
				maxPage = max(int(m[0]), maxPage)
		
	if len(m) > 0:
		return maxPage
	else:
		return None


if __name__ == "__main__":
	#path_exists = Path.exists(dest_path)
	path_exists = True
	if path_exists:
		print('Destination path: ' + dest_path)
		for i in range(1,4):
			page_url = author_url + 'page/' + str(i) + '/'
			#print(page_url)
			getBlogs(page_url,dest_path)
	else:
		print(f'Path {dest_path} does not exist!')
