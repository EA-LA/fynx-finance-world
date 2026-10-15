from pathlib import Path
import re,html,json
root=Path(__file__).resolve().parents[1];base='https://ea-la.github.io/fynx-finance-world';urls=[]
for p in root.glob('*.html'):
 s=p.read_text();private=p.name in ['admin-login.html','dashboard.html']
 s=re.sub(r'<!-- search-identity:start -->.*?<!-- search-identity:end -->','',s,flags=re.S)
 s=re.sub(r'<link\b[^>]*rel=["\']canonical["\'][^>]*>','',s,flags=re.I)
 s=re.sub(r'<meta\b[^>]*(?:name=["\']robots["\']|property=["\']og:(?:title|description|url|type)["\'])[^>]*>','',s,flags=re.I)
 title=html.unescape(re.search('<title>(.*?)</title>',s,re.S)[1]);desc=html.unescape(re.search('<meta name="description" content="([^"]*)"',s)[1]);url=base+('/' if p.name=='index.html' else '/'+p.name)
 tags=f'<meta name="robots" content="{"noindex,follow" if private else "index,follow,max-image-preview:large"}"><link rel="canonical" href="{url}">'
 for k,v in [('title',title),('description',desc),('url',url),('type','website')]:tags+=f'<meta property="og:{k}" content="{html.escape(v,quote=True)}">'
 if not private:
  urls.append(url);org={'@type':'Organization','@id':'https://www.fynxfinanceworld.com/#organization','name':'FYNX','url':'https://www.fynxfinanceworld.com/','founder':{'@type':'Person','@id':'https://ea-la.github.io/#person','name':'Elham Amini','url':'https://ea-la.github.io/'}}
  graph=[org,{'@type':'WebSite','@id':base+'/#website','name':'Fynx Money Management','url':base+'/','publisher':{'@id':org['@id']}},{'@type':'WebPage','@id':url+'#webpage','name':title,'description':desc,'url':url,'isPartOf':{'@id':base+'/#website'}}]
  tags+='<script type="application/ld+json">'+json.dumps({'@context':'https://schema.org','@graph':graph}).replace('<','\\u003c')+'</script>'
 s=s.replace('</head>','<!-- search-identity:start -->'+tags+'<!-- search-identity:end --></head>')
 if not private and 'href="https://ea-la.github.io/"' not in s:s=s.replace('</footer>','<p style="max-width:1040px;margin:24px auto;padding:0 32px"><a href="https://ea-la.github.io/">Elham Amini, founder</a> · <a href="https://www.fynxfinanceworld.com/about.html">About FYNX</a></p></footer>')
 p.write_text(s)
(root/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+u+'</loc></url>' for u in urls)+'</urlset>\n')
(root/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+base+'/sitemap.xml\n')
print(len(urls),'public pages; owner and dashboard excluded.')
