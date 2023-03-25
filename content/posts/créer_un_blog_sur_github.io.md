---
title: "Créer un Blog sur github.io"
date: 2023-03-25T16:55:39+01:00
tags: ["Hugo","SSG"]
---

Créer un repo BlogSources.

Créer un repo Bigsmooth68.github.io. Activer github pages pour ce repo.

```bash
hugo new site BlogSources
```

```bash
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/Bigsmooth68/BlogSources.git
git push -u origin main
```

.gitignore file:
```bash
https://www.toptal.com/developers/gitignore/api/visualstudiocode,hugo
```

```bash
git clone https://github.com/lukeorth/poison.git themes/poison --depth=1
```

Mettre à config.toml (notamment le thème). Lien [ici](https://github.com/Bigsmooth68/BlogSources/blob/main/config.toml).

Ajouter le repo github dans `public`:
```bash
git submodule add -f https://github.com/Bigsmooth68/Bigsmooth68.github.io public
```

Générer le site:
```bash
hugo -t poison
```

Ajouter le code généré dans le repo 
```bash
cd public
git commit -m 'Initial commit'
git push
```

Ajouter l'about:
```bash
hugo new page/about.md
```

Ajouter un post:
```bash
mkdir blog
hugo new posts/créer_un_blog_sur_github.io.md
```
