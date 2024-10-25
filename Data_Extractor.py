from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

# Initialize the SPARQL wrapper with the Wikidata endpoint
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

# Add a valid User-Agent header to comply with Wikidata's requirements
sparql.addCustomHttpHeader("User-Agent", "IsraeliActorsGrid/1.0 (omriomrinir@gmail.com)")

# Set the SPARQL query
sparql.setQuery("""
SELECT ?actorLabel ?workLabel WHERE {
  ?actor wdt:P31 wd:Q5;                         # The actor is a human
         wdt:P106/wdt:P279* wd:Q33999;          # Occupation: actor (including subclasses)
         wdt:P27 wd:Q801.                       # Country of citizenship: Israel
  ?work wdt:P161 ?actor.                        # The actor is a cast member of the work
  SERVICE wikibase:label { bd:serviceParam wikibase:language "he,en". }  # Retrieve labels in Hebrew and English
}
""")

# Set the return format to JSON
sparql.setReturnFormat(JSON)

# Execute the query and get the results
print("Executing SPARQL query...")
results = sparql.query().convert()

# Initialize an empty list to store the data
data = []

# Iterate over the results and extract the actor and work labels
print("Processing results...")
for result in results["results"]["bindings"]:
    actor = result["actorLabel"]["value"]
    work = result["workLabel"]["value"]
    data.append({"Actor Name": actor, "Work": work})

print(f"Total records retrieved: {len(data)}")

# Convert the data into a DataFrame
df = pd.DataFrame(data)

# Group the works by actor and aggregate them into a comma-separated string
print("Organizing data...")
actor_filmography = df.groupby('Actor Name')['Work'].apply(lambda x: ', '.join(sorted(set(x)))).reset_index()

# Sort the actors alphabetically (optional)
actor_filmography = actor_filmography.sort_values('Actor Name').reset_index(drop=True)

# Display the first few rows (optional)
print(actor_filmography.head())

# Save the data to an Excel file
print("Saving data to 'actors_filmography.xlsx'...")
actor_filmography.to_excel('actors_filmography.xlsx', index=False)

# Or save to a CSV file with UTF-8 encoding
print("Saving data to 'actors_filmography.csv'...")
actor_filmography.to_csv('actors_filmography.csv', index=False, encoding='utf-8-sig')

print("Data saved successfully.")
