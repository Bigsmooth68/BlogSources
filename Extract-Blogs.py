import requests, os
from pathlib import Path
from bs4 import BeautifulSoup
from colorama import Fore, Style
from git import Repo

root_url = 'https://www.dbi-services.com/blog/'
author_url = root_url + 'author/ols/'
dest_path = 'content\dbi-blogs\\'

def getBlogs(url,destination):
	currentPage = 1
	blogsCount = 0

	m = []
	nextpage = True
	while nextpage:
		
		currentUrl = url + str(currentPage) + '/'
		response = requests.get(currentUrl)
		if response.status_code == 404:
			print(f'\n {currentPage-1} pages processed.')
			return 0
		print(f'\nProcessing page {currentPage}')
		html_text = response.text
		soup = BeautifulSoup(html_text,'html.parser')

		for link in soup.find_all('a',href=True,):
			lk = link.get('href')
			lkClass = link.get('class')
			if 'https://www.dbi-services.com/blog/' in lk:
				if 'text-decoration-none' in lkClass:
					title = link.h2.string.strip()
					sanitized_title = lk.replace(root_url,'').replace('/','')
					infos = (link.find('div',class_='infos')).text
					publishedDateStr = infos.split(' ')[0]
					publishedDateArray = publishedDateStr.split('.')
					publishedDate = f'{publishedDateArray[2]}-{publishedDateArray[1]}-{publishedDateArray[0]}'
					pubDateStr = str(publishedDate)
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
						blogsCount += 1
					else:
						print(f'{sanitized_title} {Fore.RED}ignored{Fore.RESET}.')
						return blogsCount
				
		currentPage += 1
	return blogsCount

#########

if __name__ == "__main__":
	#path_exists = Path.exists(dest_path)
	path_exists = True
	if path_exists:
		print('Destination path: ' + dest_path)
		page_url = author_url + 'page/'
		#print(page_url)
		newBlogsCount = getBlogs(page_url,dest_path)
	else:
		print(f'Path {dest_path} does not exist!')

print(f'{newBlogsCount} new blog(s) found.')

# newBlogsCount = 1 ## fake
if (newBlogsCount > 0):
	print('Calling hugo: ', end='', flush=True)
	stream = os.popen('hugo')
	hugoOutput = stream.read()
	print(Fore.GREEN + 'OK' + Style.RESET_ALL)

	# Add files to git
	# print('Initiating git repo object')
	# repo = Repo('.')
	# print('Add files to repo')
	# repo.index.add('.')