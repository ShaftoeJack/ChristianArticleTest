import json

with open('citations_index.json', 'r') as f:
    data = json.load(f)
    
print('Quality check of citations:')
good_citations = 0
for i in range(min(10, len(data['citations']))):
    cite = data['citations'][i]
    if cite['authors'] and len(cite['authors']) > 10 and cite['year'] and cite['title'] != 'Title not extracted':
        good_citations += 1
    print(f'\nCitation {cite["id"]}:')
    print(f'  Authors: {cite["authors"][:80]}...')
    print(f'  Year: {cite["year"]}')
    print(f'  Title: {cite["title"][:80]}...')
    print(f'  Journal: {cite["journal"]}')

print(f'\nQuality metrics from first 10:')
print(f'Good quality citations: {good_citations}/10')
print(f'Total citations in database: {len(data["citations"])}')

# Check for well-formatted citations
well_formatted = 0
for cite in data['citations']:
    if (cite['authors'] and len(cite['authors']) > 5 and 
        cite['year'] and cite['year'] > 1800 and 
        cite['title'] and cite['title'] != 'Title not extracted' and 
        cite['journal'] and len(cite['journal']) > 3):
        well_formatted += 1

print(f'Total well-formatted citations: {well_formatted}/{len(data["citations"])} ({well_formatted/len(data["citations"])*100:.1f}%)')