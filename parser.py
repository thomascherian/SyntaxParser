root={}
inflected={}
aux=["am", "are","is","was","were","being","be","been","can","could","do","did","does","doing","have","had","has","having","may","might","must","shall","should","will","would"]
pos_pro=["its","my","mine","your","her","hers","his","our","ours","their","theirs","yours"]
outp=open("parser_out.txt","w")


def main():
	count=0
	new_count=0
	partial_count=0
	root_miss_count=0
	new_sent=[]
	partial_t=[]
	root_miss_sent=[]
	with open('corpus.txt') as fp:
		for line in fp:
			count=count+1
			words=line.split()
			i=0
			while(i<len(words)):
				words[i]=words[i].strip('.')
				i=i+1
			print("-------------------------")
			print(words)
			outp.write("\n-------------------------\n")
			for word in words:
				outp.write("|"+word+"|")
			tree=[]
			visited=[]
			newword=[]
			tags=[]
		
			for word in words:
    				visited.append(0)
    				if(word.capitalize() in root):
        				tags.append(root[word.capitalize()])
    				elif(word.capitalize() in inflected):
        				tags.append(inflected[word.capitalize()])
    				else:
        				tags.append("u")
			print(tags)
			outp.write("\n")
			for tag in tags:
				outp.write("|"+tag+"|")
			flags=parser(tags,words,tree,visited,newword)			

			if(flags[0]==1):
                		partial_count=partial_count+1
                		partial_t.append(line)
        		if(flags[1]==1):
                		new_count=new_count+1
                		new_sent.append(line)
        		if(flags[2]==1):
                		root_miss_count=root_miss_count+1
                		root_miss_sent.append(line)

			print("------------------------")
	outp.write("\n\n**************************************************\n");
	outp.write("\n Total number of sentences\t:"+str(count))
	outp.write("\n Complete parse trees\t:"+str(count-partial_count-root_miss_count))
	outp.write("\n Incomplete parse trees with unknown relations\t:"+str(partial_count))
	outp.write("\n Failed due to the lack of root verb in the sentence\t:"+str(root_miss_count))
	outp.write("\n Number of sentences with new words\t:"+str(new_count))
	outp.write("\n\n Sentences for which parse tree is incomplete: \n")
	if(len(partial_t)>0):
		for s in partial_t:
			outp.write("\t"+s)
	else:
		outp.write("\tNone")
	outp.write("\n\n Sentences where the root verb is missing: \n")
	if(len(root_miss_sent)>0):
		for s in root_miss_sent:
			outp.write("\t"+s)
	else:
		outp.write("\tNone")
	outp.write("\n\n Sentences with new words: \n")
	if(len(new_sent)>0):
		for s in new_sent:
			outp.write("\t"+s)
	else:
		outp.write("\tNone")



with open('RootDict.txt') as fp:
    for line in fp:
      a=line.split('/')
      a[1]=a[1].strip()
      root[a[0]]=a[1]
with open('InflectedDict.txt') as fp:
    for line in fp:
      a=line.split('/')
      a[1]=a[1].strip()
      inflected[a[0]]=a[1]

def verb(start,end,tags):
	i=start
	while(i<=end):
		if(tags[i]=="v"):
			return i
		i=i+1
	return -1

def preposition(start,end,tags):
	i=start
	while(i>=end):
		if(tags[i]=="prep"):
			return i
		i=i-1
	return -1

def posess_pronoun(start,end,tags,words):
	i=start
	while(i>=end):
		if((tags[i]=="pron") and (words[i].lower() in pos_pro)):
			return i
		i=i-1
	return -1

def nounl(start,end,tags,visited,tree,words):
	i=start
	ind=-1
	while(i>=end):
		if(tags[i]=="n" or ((tags[i]=="pron")and (words[i].lower() not in pos_pro))):
			ind=i
			break
		i=i-1
	if(ind!=-1):
		posprn=posess_pronoun(ind-1,end,tags,words)
		if((posprn!=-1) and (visited[posprn]==0)):
			tree.append("posess("+words[ind]+"-"+str(ind)+","+words[posprn]+"-"+str(posprn)+")")
			visited[posprn]=1
		detm=det(ind-1,end,tags)	
		if((detm!=-1) and (visited[detm]==0)):
			tree.append("det("+words[ind]+"-"+str(ind)+","+words[detm]+"-"+str(detm)+")")
			visited[detm]=1
		adj=adjective(ind-1,end,tags)
		if((adj!=-1) and (visited[adj]==0)):
			tree.append("adj("+words[ind]+"-"+str(ind)+","+words[adj]+"-"+str(adj)+")")
			visited[adj]=1			
			
	return ind

def nounr(start,end,tags,visited,tree,words):
	i=start
	ind=-1
	while(i<=end):
		if(tags[i]=="n" or ((tags[i]=="pron")and (words[i].lower() not in pos_pro))):
			ind=i
			break
		i=i+1
	if((ind<end)and(ind!=-1)):
		if(tags[ind]=="n" and tags[ind+1]=="n"):
			tree.append("NN("+words[ind+1]+"-"+str(ind+1)+","+words[ind]+"-"+str(ind)+")")
                	visited[ind]=1
			ind=ind+1

	if(ind!=-1):
		posprn=posess_pronoun(ind-1,start,tags,words)
                if((posprn!=-1) and (visited[posprn]==0)):
                        tree.append("posess("+words[ind]+"-"+str(ind)+","+words[posprn]+"-"+str(posprn)+")")
                        visited[posprn]=1
		detm=det(ind-1,start,tags)
		if((detm!=-1) and (visited[detm]==0)):
			tree.append("det("+words[ind]+"-"+str(ind)+","+words[detm]+"-"+str(detm)+")")
			visited[detm]=1
		adj=adjective(ind-1,start,tags)
		if((adj!=-1) and (visited[adj]==0)):
			tree.append("adj("+words[ind]+"-"+str(ind)+","+words[adj]+"-"+str(adj)+")")
			visited[adj]=1
		prep=preposition(ind-1,start,tags)
		if((prep!=-1) and (visited[prep]==0)):
			tree.append("case("+words[ind]+"-"+str(ind)+","+words[prep]+"-"+str(prep)+")")
                        visited[prep]=1
			tree.append("nmod("+words[start-1]+"-"+str(start-1)+","+words[ind]+"-"+str(ind)+")")
                        visited[ind]=1
	return ind

def det(start,end,tags):
	i=start
	while(i>=end):
		if(tags[i]=="article"):
			return i
		i=i-1
	return -1

def adjective(start,end,tags):
	i=start
	while(i>=end):
		if(tags[i]=="adj"):
			return i
		i=i-1
	return -1

def adverb(start,end,tags):
	i=start
	while(i<=end):
		if(tags[i]=="adv"):
			return i
		i=i+1
	return -1

def parser(tags,words,tree,visited,newword):

	unknown_flag=0
	new_w_flag=0
	root_flag=0	
	n=len(tags)
	root=verb(0,n-1,tags)
	while(root!=-1):
		if(words[root] not in aux):
			v=0
			while(v<n):
				if((v!=root)and(tags[v]=="v") and (words[v] in aux)):
					visited[v]=1
		                        tree.append("aux("+words[root]+"-"+str(root)+","+words[v]+"-"+str(v)+")")			
				v=v+1
			break
		root=verb(root+1,n-1,tags)
	if(root==-1):
		root=verb(0,n-1,tags)
	if((root!=-1) and (visited[root]==0)):
		visited[root]=1
		tree.append("root("+words[root]+"-"+str(root)+")")
		
		subj=nounl(root-1,0,tags,visited,tree,words)
		if((subj!=-1) and (visited[subj]==0)):
			visited[subj]=1
			tree.append("subject("+words[root]+"-"+str(root)+","+words[subj]+"-"+str(subj)+")")
		verb2=verb(root+1,n-1,tags)
		if((verb2!=-1) and (visited[verb2]==0)):
			visited[verb2]=1
			tree.append("verb2("+words[root]+"-"+str(root)+","+words[verb2]+"-"+str(verb2)+")")
			obj=nounr(verb2+1,n-1,tags,visited,tree,words)
			if((obj!=-1) and (visited[obj]==0)):
				visited[obj]=1
				tree.append("object("+words[verb2]+"-"+str(verb2)+","+words[obj]+"-"+str(obj)+")")
			adv=adverb(verb2-1,n-1,tags)
			if((adv!=-1) and (visited[adv]==0)):
				visited[adv]=1
				tree.append("advmod("+words[verb2]+"-"+str(verb2)+","+words[adv]+"-"+str(adv)+")")
			adv=adverb(verb2+1,n-1,tags)
                        if((adv!=-1) and (visited[adv]==0)):
                                visited[adv]=1
                                tree.append("advmod("+words[verb2]+"-"+str(verb2)+","+words[adv]+"-"+str(adv)+")")
	
		obj=nounr(root+1,n-1,tags,visited,tree,words)
		if((obj!=-1) and (visited[obj]==0)):
			visited[obj]=1
			tree.append("object("+words[root]+"-"+str(root)+","+words[obj]+"-"+str(obj)+")")
			dummy=nounr(obj+1,n-1,tags,visited,tree,words)
			if((dummy!=-1)and visited[dummy]==0):
				print("\nError: 2 objects");
	
		elif(obj==-1):
			adjsub=adjective(n-1,root+1,tags)
			if(adjsub!=-1):
				visited[adjsub]=1
				tree.append("adjsub("+words[subj]+"-"+str(subj)+","+words[adjsub]+"-"+str(adjsub)+")")			
		adv=adverb(root-1,n-1,tags)
		if((adv!=-1) and (visited[adv]==0)):
			visited[adv]=1
			tree.append("advmod("+words[root]+"-"+str(root)+","+words[adv]+"-"+str(adv)+")")
		adv=adverb(root+1,n-1,tags)
                if((adv!=-1) and (visited[adv]==0)):
                        visited[adv]=1
                        tree.append("advmod("+words[root]+"-"+str(root)+","+words[adv]+"-"+str(adv)+")")


		k=0
		while(k<n):
			if(visited[k]==0):
				unknown_flag=1
				tree.append("unknown("+words[root]+"-"+str(root)+","+words[k]+"-"+str(k)+")")
			k=k+1
		k=0
		while(k<n):
			if(tags[k]=="u"):
				new_w_flag=1
				newword.append(words[k])
			k=k+1
			
		print("\nParser output:\n")
		print(tree)
		print("\nNew words:\t")
		outp.write("\nParser output: \n")
		for tr in tree:
			outp.write("\t"+tr+"\n")
		outp.write("\nNew words: \t")
		if(len(newword)>0):
			print(newword)
			for w in newword:
				outp.write("|"+w+"|")
			outp.write("\n")
		else:
			print("None\n")	
			outp.write("None\n")
				
	else:
		print("Parse ERROR: Root does not exists\n")
		outp.write("Parse ERROR: Root does not exists\n")
		root_flag=1
	flags=[unknown_flag,new_w_flag,root_flag]
	return flags


main()
